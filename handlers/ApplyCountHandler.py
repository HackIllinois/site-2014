from db.Attendee import Attendee
from db import constants
import logging
import MainHandler

from google.appengine.api import memcache

page = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>HackIllinois</title>
</head>
<body>
    <p>%d %s</p>
</body>
</html>
"""

class ApplyCountHandler(MainHandler.Handler):
    def get(self):
        cached_count = memcache.get('apply_count')
        s = '(memcache &#9786; )'

        if cached_count is None:
            s = '(datastore &#9785; )'
            q = Attendee.query(Attendee.isRegistered == True)
            cached_count = q.count()
            if not memcache.set('apply_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Apply Count:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.write(page % (cached_count, s))
