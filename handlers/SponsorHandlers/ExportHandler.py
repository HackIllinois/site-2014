import logging
import csv
import cStringIO

import urllib
        
from google.appengine.api import memcache
        
import MainSponsorHandler
from db import constants
import datetime

class ExportHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self, status=None, category=None, route=None):
        sponsor_user = self.get_sponsor_user()
        logging.error("NO ERROR HERE1")
        if not sponsor_user: return self.abort(500, detail='User not in database')
        if not sponsor_user.attendeeDataAccess:
            return self.abort(401, detail='User does not have permission to download attendees csv.')

        if status is not None:
            status = str(urllib.unquote(status))
            if status not in constants.STATUSES + ['All', 'a', 'b', 'c']:
                return self.abort(404, detail='Status <%s> does not exist.' % status)
        if category is not None:
            category = str(urllib.unquote(category))
            if category not in constants.CATEGORIES:
                return self.abort(404, detail='Category <%s> does not exist.' % category)
        if route is not None:
            route = str(urllib.unquote(route))
            if category != constants.TRAVEL_RIDE_BUS:
                return self.abort(404, detail='Incorrect category <%s>.' % category)
            if route not in constants.BUS_ROUTES:
                return self.abort(404, detail='Route <%s> does not exist.' % route)
        logging.error("NO ERROR HERE1")
        data = self.get_hackers_csv_memcache(self.request.application_url, status, category, route, constants.USE_SPONSOR_MEMCACHE)

        dt = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment;filename=' + dt + '-attendees.csv'
        return self.write(data)

    def get_hackers_csv_memcache(self, base_url, status, category, route, use_memcache=True):
        """Gets the 'hackers_csv' key from the memcache and updates the memcache if the key is not in the memcache"""
        if use_memcache:
            csv_string = memcache.get('hackers_csv/' + str(status) + '/' + str(category) + '/' + str(route))
            if csv_string is None or not use_memcache:
                csv_string = self.set_hackers_csv_memcache(base_url, status, category, route)
            return csv_string
        else:
            return self.set_hackers_csv_memcache(base_url, status, category, route)

    def set_hackers_csv_memcache(self, base_url, status, category, route):
        # hackers = self.get_hackers_new_memcache(status, category, route, constants.USE_ADMIN_MEMCACHE)
        hackers = self.get_hackers_better_memcache(status, category, route)
        output = cStringIO.StringIO()
        writer = csv.writer(output)

        fields = ['nameFirst','nameLast','email','school','year']

        csv_headings = ['First Name','Last Name','Email','School','Year', 'Resume', 'Is Attending']

        writer.writerow(csv_headings)
        for h in hackers:
            row = []
            for f in fields:
                if f in h and h[f] is not None:
                    row.append(h[f])
                else:
                    row.append('')

            if 'resume' in h and h['resume'] is not None:
                row.append(base_url + '/corporate/resume?userId='+h['userId'])
            else:
                row.append('')

            if 'approvalStatus' in h and h['approvalStatus'] is not None and h['approvalStatus']['status'] is not None:
                if h['approvalStatus']['status'] == "Rsvp Coming":
                    row.append("Yes")
                else:
				    row.append("No")
            else:
                row.append('')

            writer.writerow(row)

        csv_string = output.getvalue()
        output.close()

        if not memcache.set('hackers_csv/' + str(status) + '/' + str(category) + '/' + str(route), csv_string, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return csv_string