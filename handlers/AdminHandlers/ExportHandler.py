import logging
import csv
import cStringIO

from google.appengine.api import memcache

import MainAdminHandler
from db import constants
import datetime

class ExportHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to download attendees csv.')

        dt = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment;filename=' + dt + '-attendees.csv'

        return self.write(self.get_hackers_csv_memcache(self.request.application_url))


    def set_hackers_csv_memcache(self, base_url):
        hackers = self.get_hackers_memecache()
        output = cStringIO.StringIO()
        writer = csv.writer(output)

        fields = ['nameFirst','nameLast','email',
                  'gender','school','year','linkedin',
                  'github','shirt','food','projectType',
                  'registrationTime','isApproved','userId']

        writer.writerow(constants.CSV_HEADINGS)
        for h in hackers:
            row = []
            for f in fields:
                if f in h and h[f] is not None:
                    row.append(h[f])
                else:
                    row.append('')
            if 'resume' in h and h['resume'] is not None:
                row.append(base_url + '/admin/resume?userId='+h['userId'])
            else:
                row.append('')

            writer.writerow(row)

        csv_string = output.getvalue()
        output.close()

        if not memcache.add('hackers_csv', csv_string, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return csv_string


    def get_hackers_csv_memcache(self, base_url):
        """Gets the 'hackers_csv' key from the memcache and updates the memcache if the key is not in the memcache"""
        csv_string = memcache.get('hackers_csv')
        if not csv_string:
            csv_string = self.set_hackers_csv_memcache(base_url)

        stats = memcache.get_stats()
        logging.info('Hackers CSV:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        return csv_string