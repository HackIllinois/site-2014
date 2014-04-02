import MainAdminHandler
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache

import logging
import urllib
from collections import defaultdict

class BasicStatsHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, status=None):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        if status is not None:
            status = str(urllib.unquote(status))
            if status not in constants.STATS_STATUSES:
                return self.abort(404, detail='Status <%s> does not exist.' % status)

        data = self.get_basic_stats_memcache(status, constants.USE_ADMIN_MEMCACHE)

        if status is None: data['status_dropdown_text'] = 'All Hackers'
        elif status == 'approved': data['status_dropdown_text'] = 'Approved Hackers'
        elif status == 'emailed': data['status_dropdown_text'] = 'Emailed Hackers'
        elif status == 'rsvpd': data['status_dropdown_text'] = 'RSVP\'d Hackers'
        else: data['status_dropdown_text'] = 'Select One...'

        return self.render('basic_stats.html', data=data, approveAccess=admin_user.approveAccess, mobileAccess=admin_user.mobileAccess, fullAccess=admin_user.fullAccess)

    def get_basic_stats_memcache(self, status, use_memcache=False):
        """Gets the 'basic_stats' key from memcache"""
        if use_memcache:
            data = memcache.get('basic_stats/'+str(status))
            if data is None:
                data = self.set_basic_stats_memcache(status)
            return data
        else:
            return self.set_basic_stats_memcache(status)

    def set_basic_stats_memcache(self, status):
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

        status_map = {
            'approved': 'Approved',
            'emailed': 'Awaiting Response',
            'rsvpd': 'Rsvp Coming'
        }
        hackers = None
        if status is None:
            hackers = Attendee.query(Attendee.isRegistered == True, ancestor=Attendee.get_default_event_parent_key())
        else:
            hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status_map[status], ancestor=Attendee.get_default_event_parent_key())

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
        data['fields'] = []

        ordered_fields = ['Genders', 'Projects', 'Years', 'Travel', 'Resume', 'Team', 'Shirts', 'Diets', 'Schools']
        for field in ordered_fields:
            d = {}
            d['name'] = field
            d['stats'] = []
            for option in sorted(collected[field].keys()):
                e = {}
                e['name'] = option
                e['num'] = collected[field][option]
                d['stats'].append(e)
            data['fields'].append(d)

        if not memcache.set('basic_stats/'+str(status), data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return data