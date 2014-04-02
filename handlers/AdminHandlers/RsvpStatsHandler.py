import MainAdminHandler
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache

import logging
import urllib
from collections import defaultdict
from itertools import izip

class RsvpStatsHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, status=None):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = {}
        data['tables'] = self.get_rsvp_stats_memcache(constants.USE_ADMIN_MEMCACHE)

        return self.render('admin_rsvp_stats.html', data=data, approveAccess=admin_user.approveAccess, mobileAccess=admin_user.mobileAccess, fullAccess=admin_user.fullAccess)

    def get_rsvp_stats_memcache(self, use_memcache=True):
        """Gets the 'rsvp_stats' key from memcache"""
        if use_memcache:
            data = memcache.get('rsvp_stats')
            if data is None:
                data = self.set_rsvp_stats_memcache()
            return data
        else:
            return self.set_rsvp_stats_memcache()

    def set_rsvp_stats_memcache(self):
        """Sets the 'rsvp_stats' key in memcache"""
        # Status: RSVP Yes, No, No Response
        # Hardware
        # Microcontrollers 1: Arduinos, Raspberry Pi
        # Microcontrollers 1: Electric Imp Dev Kit, Spark Core
        # Lab Equipment: Power Supplies, Oscilloscopes
        # Travel Arrangements, Bus Route

        # {'name':'','stats':[{'name':'','num':0}],'totalCount':0}

        tables = []

        # Status Table
        q = Attendee.query(Attendee.approvalStatus.status.IN(['Rsvp Coming', 'Rsvp Not Coming', 'No Rsvp']), Attendee.isRegistered == True, ancestor=Attendee.get_default_event_parent_key())
        t = {}
        t['name'] = 'RSVP Status'
        t['stats'] = []
        for status in ['Rsvp Coming', 'Rsvp Not Coming', 'No Rsvp']:
            count = q.filter(Attendee.approvalStatus.status == status).count()
            t['stats'].append({'name':status, 'num':count})
        t['totalCount'] = sum([i['num'] for i in t['stats']])
        tables.append(t)


        hardware_totals = defaultdict(int)
        lab_totals = defaultdict(int)
        hardware_m1 = defaultdict(int)
        hardware_m2 = defaultdict(int)
        lab = defaultdict(int)
        travel = defaultdict(int)
        bus = defaultdict(int)

        q = Attendee.query(Attendee.approvalStatus.status =='Rsvp Coming', Attendee.isRegistered == True, ancestor=Attendee.get_default_event_parent_key())
        for hacker in q:
            hardware_m1[hacker.micro1] += 1
            hardware_m2[hacker.micro2] += 1
            lab[hacker.labEquipment] += 1
            travel[hacker.travel] += 1

            if hacker.busRoute is not '':
                bus[hacker.busRoute] += 1

            if hacker.micro1 is not '':
                for i in hacker.micro1.split(','):
                    hardware_totals[i] += 1

            if hacker.micro2 is not '':
                for i in hacker.micro2.split(','):
                    hardware_totals[i] += 1

            if hacker.labEquipment is not '':
                for i in hacker.labEquipment.split(','):
                    lab_totals[i] += 1


        all_tables = [hardware_totals, lab_totals, hardware_m1, hardware_m2, lab, travel, bus]
        table_names = ['Hardware Totals', 'Lab Equipment Totals', 'Microcontrollers - Return', 'Microcontrollers - Keep', 'Lab Equipment', 'Travel Arrangements', 'Bus Routes']

        for table, name in izip(all_tables, table_names):
            t = {}
            t['name'] = name
            t['stats'] = []
            for option in sorted(table.keys()):
                if option == '':
                    t['stats'].append({'name':'None', 'num':table[option]})
                else:
                    t['stats'].append({'name':option, 'num':table[option]})
            t['totalCount'] = sum([i['num'] for i in t['stats']])
            tables.append(t)

        if not memcache.set('rsvp_stats', tables, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return tables
