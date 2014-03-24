import MainAdminHandler
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache

import logging

class SchoolCountHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        cached_count = self.get_school_count_memcache(constants.USE_ADMIN_MEMCACHE)
        return self.write('%d' % cached_count)

    def get_school_count_memcache(self, use_memcache=False):
        """Gets the 'school_count' key from memcache"""
        cached_count = memcache.get('school_count')
        if cached_count is None or not use_memcache:
            cached_count = self.set_school_count_memcache()
        return cached_count

    def set_school_count_memcache(self):
        """Sets the 'school_count' key in memcache"""
        q = Attendee.query(Attendee.isRegistered == True, projection=[Attendee.school], distinct=True)
        set_of_field = set([data.school for data in q])
        cached_count = len(set_of_field)
        if not memcache.add('school_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return cached_count