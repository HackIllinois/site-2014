import MainAdminHandler
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache

import logging

class BusRouteStatsHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = memcache.get('bus_route_stats')

        if not data:
            bus_routes = [
                {
                    'routeName': 'Purdue',
                    'schools': ['Purdue University'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'Iowa State -> Grinnell -> University of Iowa',
                    'schools': ['Iowa State University', 'University of Iowa', 'Grinnell College'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'Northwestern -> University of Chicago',
                    'schools': ['Northwestern University', 'University of Chicago'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'Illinois Institute of Technology -> University of Illinois Chicago -> Depaul',
                    'schools': ['Illinois Institute of Technology', 'Depaul University', 'University of Illinois - Chicago', 'university of illinois at chicago'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'Michigan Tech -> UW Madison',
                    'schools': ['Michigan Technological University', 'Michigan Institute of Technology', 'Michigan Tech', 'Michigan Tech University', 'University of Wisconsin', 'University of Wisconsin - Madison', 'UW Madison', 'UW-Madison'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'IU Bloomington -> Rose-Hulman',
                    'schools': ['Indiana University Bloomington', 'Indiana University', 'Rose Hulman Institute of Technology'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'University of Missouri (Columbia) -> Washington University',
                    'schools': ['University of Missouri - Columbia', 'University of Missouri', 'Washington University in St. Louis'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'Case Western Reserve -> Kent State -> Ohio State',
                    'schools': ['Case Western Reserve University', 'kent state university', 'Kent state university', 'Kent State University', 'Kent State University', 'Ohio State University'],
                    'riderCount': 0,
                },
                {
                    'routeName': 'University of Michigan (+Purdue overflow, not counted here)',
                    'schools': ['Ann Arbor', 'University of Michigan'],
                    'riderCount': 0,
                },
            ]

            # Put routes in a school name --> route map to speed up the query over everyone
            school_to_routes = {}
            for bus_route in bus_routes:
                for school in bus_route['schools']:
                    if not school in school_to_routes:
                        school_to_routes[school] = [bus_route]
                    else:
                        school_to_routes[school].append(bus_route)

            # Count the riders
            hackers = Attendee.search_database({'isRegistered':True})
            for hacker in hackers:

                # We assume everyone who has not marked a travel preference is coming via a bus
                if (hacker.travel == constants.TRAVEL_RIDE_BUS or hacker.travel == '') and hacker.school in school_to_routes:
                    for route in school_to_routes[hacker.school]:
                        route['riderCount'] += 1

            data = bus_routes

            if not memcache.add('bus_route_stats', data, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Basic Stats:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        return self.render('bus_stats.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)