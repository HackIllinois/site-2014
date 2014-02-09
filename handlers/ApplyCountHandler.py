from db.Attendee import Attendee
import MainHandler

from google.appengine.api import memcache

class ApplyCountHandler(MainHandler.Handler):
    def get(self):
        cached_count = memcache.get('apply_count')

        if cached_count:
            self.write('%s (read from memcache for freeeee!)' % cached_count)
        else:
            q = Attendee.query(Attendee.isRegistered == True)
            count = q.count()
            memcache.set('apply_count', count)

            self.write('%d (and you made us do a query :( )' % count)