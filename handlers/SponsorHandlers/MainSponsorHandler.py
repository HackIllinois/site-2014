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
        if not self.db_user: return self.redirect('/corp/notregistered')

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


    # http://stackoverflow.com/questions/7111068/split-string-by-count-of-characters
    def chunks(self, s, n):
        """Produce `n`-character chunks from `s`."""
        for start in range(0, len(s), n):
            yield s[start:start+n]

    """http://stackoverflow.com/questions/9127982/avoiding-memcache-1m-limit-of-values"""
    def store(self, key, value, chunksize=950000):
        serialized = pickle.dumps(value)
        values = {}
        i = 0
        for chunk in self.chunks(serialized, chunksize):
            values['%s.%s' % (key, i)] = chunk
            i += 1
        memcache.set_multi(values, time=constants.MEMCACHE_TIMEOUT)

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

    def get_hackers_memcache(self, isAttending=None):
        """Gets the 'sponsor/hackers/<isAttending>' key in the memcache"""
        key = 'sponsor/hackers/' + str(isAttending)
        data = self.retrieve(key)

        stats = memcache.get_stats()
        logging.info('Cache Hits:%s, Cache Misses:%s' % (stats['hits'], stats['misses']))

        if data is None:
            data =  self.set_hackers_memcache(isAttending)

        return data

    def set_hackers_memcache(self, isAttending=None):
        """Sets the 'sponsor/hackers/<isAttending>' key in the memcache"""
        key = 'sponsor/hackers/' + str(isAttending)
        hackers = None

        if isAttending is None:
            hackers = Attendee.query(Attendee.isRegistered == True,
                                     ancestor=Attendee.get_default_event_parent_key())
        elif isAttending is True:
            hackers = Attendee.query(Attendee.isRegistered == True,
                                     Attendee.approvalStatus.status == 'Rsvp Coming',
                                     ancestor=Attendee.get_default_event_parent_key())
        else:
            hackers = Attendee.query(Attendee.isRegistered == True,
                                     Attendee.approvalStatus.status != 'Rsvp Coming',
                                     ancestor=Attendee.get_default_event_parent_key())

        data = {}
        for hacker in hackers:
            data[hacker.userId] = {
                'nameFirst': hacker.nameFirst,
                'nameLast': hacker.nameLast,
                'email': hacker.email,
                'school': hacker.school,
                'year': hacker.year,
                'linkedin': hacker.linkedin,
                'github': hacker.github,
                'resumeLocation': hacker.resume.gsObjectName[17:] if hacker.resume and hacker.resume.gsObjectName else None,
                'hasResume': True if hacker.resume and hacker.resume.gsObjectName else False,
                'userId': hacker.userId,
                'isAttending': True if hacker.approvalStatus and hacker.approvalStatus.status == 'Rsvp Coming' else False,
            }

        self.store(key, data)
        return data
