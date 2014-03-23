import MainAdminHandler
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache

import logging

class ApplyCountHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        cached_count = memcache.get('apply_count')

        if cached_count is None:
            q = Attendee.query(Attendee.isRegistered == True)
            cached_count = q.count()
            if not memcache.add('apply_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Apply Count:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.write('%d' % cached_count)