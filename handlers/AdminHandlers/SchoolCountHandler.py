import MainAdminHandler
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache

import logging

class SchoolCountHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        cache_key = 'school_count'
        cached_count = memcache.get(cache_key)

        if cached_count is None:
            q = Attendee.query(Attendee.isRegistered == True, projection=[Attendee.school], distinct=True)
            set_of_field = set([data.school for data in q])
            cached_count = len(set_of_field)
            if not memcache.add(cache_key, cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('School Count:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.write('%d' % cached_count)