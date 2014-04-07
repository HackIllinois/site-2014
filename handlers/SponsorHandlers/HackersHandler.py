import MainSponsorHandler
from db import constants
import json

import logging
import csv
import cStringIO
import random
import pickle

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from db.Attendee import Attendee

class HackersHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self, id=None):
        me = self.db_user

        if id:
            # TODO: profile page
            return self.write(id)

        else:
            data = {}
            hackers = self.get_hackers_memcache()
            data['hackers'] = [ hackers[i] for i in hackers ]
            data['num_people'] = len(data['hackers'])
            return self.render('sponsor/hackers.html', data=data, access=json.loads(self.db_user.access))
        
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
                'hasResume': True if hacker.resume and hacker.resume.fileName else False,
                'userId': hacker.userId,
                'isAttending': True if hacker.approvalStatus and hacker.approvalStatus.status == 'Rsvp Coming' else False,
            }

        self.store(key, data)
        return data