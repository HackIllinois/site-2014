import MainAdminHandler
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache

import logging
from collections import defaultdict

class BasicStatsHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = memcache.get('basic_stats')

        if not data or True:
            fields = {'Schools':'school', 'Genders':'gender', 'Years':'year', 'Shirts':'shirt', 'Diets':'food', 'Projects':'projectType', 'Travel':'travel'}
            resume = 'Resume'

            count = 0
            collected = {}
            for f in fields:
                collected[f] = defaultdict(int)
            collected[resume] = defaultdict(int)

            hackers = Attendee.search_database({'isRegistered':True})
            for hacker in hackers:
                count += 1
                for f in fields:
                    collected[f][getattr(hacker, fields[f])] += 1

                if hacker.resume and hacker.resume.fileName:
                    collected[resume]['Has Resume'] += 1
                else:
                    collected[resume]['No Resume'] += 1

            data = {}

            data['numPeople'] = count
            if not memcache.set('apply_count', count, time=constants.MEMCACHE_COUNT_TIMEOUT):
                logging.error('Memcache set failed.')

            data['fields'] = []

            for field in sorted(collected.keys()):
                d = {}
                d['name'] = field
                d['stats'] = []
                for option in sorted(collected[field].keys()):
                    e = {}
                    e['name'] = option
                    e['num'] = collected[field][option]
                    d['stats'].append(e)
                data['fields'].append(d)

            if not memcache.add('basic_stats', data, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Basic Stats:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        return self.render('basic_stats.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)