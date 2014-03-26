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

        data = self.get_basic_stats_memcache(constants.USE_ADMIN_MEMCACHE)
        data['num_people'] = 10
        return self.render('basic_stats.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)

    def get_basic_stats_memcache(self, use_memcache=False):
        """Gets the 'basic_stats' key from memcache"""
        data = memcache.get('basic_stats')
        if data is None or not use_memcache:
            data = self.set_basic_stats_memcache()
        return data

    def set_basic_stats_memcache(self):
        """Sets the 'basic_stats' key in memcache"""
        fields = {'Schools':'school', 'Genders':'gender', 'Years':'year', 'Shirts':'shirt', 'Diets':'food', 'Projects':'projectType', 'Travel':'travel'}
        resume = 'Resume'
        team = 'Team'

        count = 0
        collected = {}
        for f in fields:
            collected[f] = defaultdict(int)
        collected[resume] = defaultdict(int)
        collected[team] = defaultdict(int)

        hackers = Attendee.search_database({'isRegistered':True})
        for hacker in hackers:
            count += 1
            for f in fields:
                collected[f][getattr(hacker, fields[f])] += 1

            if hacker.resume and hacker.resume.fileName:
                collected[resume]['Has Resume'] += 1
            else:
                collected[resume]['No Resume'] += 1

            if hacker.teamMembers:
                collected[team]['Has Team Info'] += 1
            else:
                collected[team]['No Team Info'] += 1

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

        return data