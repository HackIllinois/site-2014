from db.Attendee import Attendee
import MainHandler

from google.appengine.api import memcache

class ApplyCountHandler(MainHandler.Handler):
    def get(self):
        cached_count = memcache.get('apply_count')

        if cached_count:
            self.write(cached_count)
            print 'read from memcache!'
        else:
            q = Attendee.query(Attendee.isRegistered == True)
            count = q.count()

            memcache.set('apply_count', count)
            print 'saving to memcache'

            self.write(count)