import logging
import csv
import cStringIO
import random
import pickle

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from handlers import MainHandler
from db import constants
from db.Attendee import Attendee
# from db.Admin import Admin
from db.Sponsor import Sponsor


class BaseSponsorHandler(MainHandler.Handler):
    """
    This is for all /sponsors pages
    Overrides the dispatch method (called before get/post/etc.)
    Sends 401 (Unauthorized) if user is not an admin
    Ref: http://webapp-improved.appspot.com/guide/handlers.html
    """

    def __init__(self, request, response):
        self.google_user = None
        self.db_user = None
        super(BaseSponsorHandler, self).__init__(request, response)

    def dispatch(self):
        self.google_user = users.get_current_user()
        if not self.google_user: return self.abort(500, detail='User not logged in')

        self.db_user = Sponsor.search_database({'userId': self.google_user.user_id()}).get()
        if not self.db_user: return self.redirect('/corporate/notregistered')

        # logging.info('%s attempted to access an admin page but was denied.', email)
        # return self.abort(401)

        logging.info('Sponsor user %s is online.', self.google_user.email())
        super(BaseSponsorHandler, self).dispatch()
		
    def get_sponsor_user(self):
        """Returns the database Sponsor model for the current logged-in user"""
        user = users.get_current_user()
        if not user:
            return None
        sponsor_user = Sponsor.search_database({'userEmail': user.email()}).get()
        if not sponsor_user:
            return None
        return sponsor_user
		
    def get_hackers_better_memcache(self, status=None, category=None, route=None):
        """Gets the 'hackers/<status>/<category>/<route>' key from the memcache and updates the memcache if the key is not in the memcache"""
        """Uses memcache for everything but the status"""
        key = 'hackers/' + str(status) + '/' + str(category) + '/' + str(route)
        data = self.retrieve(key)

        stats = memcache.get_stats()
        logging.info('Cache Hits:%s, Cache Misses:%s' % (stats['hits'], stats['misses']))

        if data is None:
            data =  self.set_hackers_better_memcache(status, category, route)
            return [ data[i] for i in data ]

        hackers = Attendee.query(
            Attendee.isRegistered == True,
            projection=[
                Attendee.userId,
                Attendee.approvalStatus.status,
                Attendee.approvalStatus.approvedTime,
                Attendee.approvalStatus.waitlistedTime,
                Attendee.approvalStatus.rsvpTime,
            ],
            ancestor=Attendee.get_default_event_parent_key()
        )
        for hacker in hackers:
            if hacker.userId not in data:
                continue
            if hacker.approvalStatus:
                data[hacker.userId]['approvalStatus'] = {
                    'status': hacker.approvalStatus.status,
                    'approvedTime': hacker.approvalStatus.approvedTime.strftime('%x %X') if hacker.approvalStatus.approvedTime else None,
                    'waitlistedTime': hacker.approvalStatus.waitlistedTime.strftime('%x %X') if hacker.approvalStatus.waitlistedTime else None,
                    'rsvpTime': hacker.approvalStatus.rsvpTime.strftime('%x %X') if hacker.approvalStatus.rsvpTime else None
                }
            else:
                data[hacker.userId]['approvalStatus'] = None
        return [ data[i] for i in data ]

		
    """http://stackoverflow.com/questions/9127982/avoiding-memcache-1m-limit-of-values"""
    def retrieve(self, key):
        MAX_SPLITS = 32
        result = memcache.get_multi(['%s.%s' % (key, i) for i in xrange(MAX_SPLITS)])
        serialized = ''
        for i in xrange(MAX_SPLITS):
            k = '%s.%s' % (key, i)
            if k not in result or not result[k]:
                break
            serialized += result[k]
        data = None
        if serialized:
            data = pickle.loads(serialized)
        return data