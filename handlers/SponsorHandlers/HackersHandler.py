import MainSponsorHandler
from db import constants
import json

import logging
import csv
import cStringIO
import random
import pickle
import urllib
from datetime import datetime

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from db.Attendee import Attendee
from db.Task import Task

class HackersHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self, key=None):
        if key:
            userId = str(urllib.unquote(key))
            db_user = Attendee.search_database({'userId':key}).get()

            hacker = {}

            text_fields = [
                'nameFirst', 'nameLast', 'email',
                'school', 'year', 'userId'
            ]

            for field in text_fields:
                value = getattr(db_user, field)
                if value is not None:
                    hacker[field] = value

            hacker['hasResume'] = True if db_user.resume and db_user.resume.fileName else False
            hacker['isAttending'] = True if db_user.approvalStatus and db_user.approvalStatus.status == 'Rsvp Coming' else False

            return self.render('sponsor/hacker_profile.html', hacker=hacker, access=json.loads(self.db_user.access))

        else:
            data = {}
            hackers = self.get_hackers_memcache(True)
            data['hackers'] = [ hackers[i] for i in hackers ]
            data['num_people'] = len(data['hackers'])
            return self.render('sponsor/hackers.html', data=data, access=json.loads(self.db_user.access))
