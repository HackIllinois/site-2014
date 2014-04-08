import MainSponsorHandler
from db import constants
import json

import logging
import csv
import cStringIO
import random
import pickle
import urllib

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from db.Attendee import Attendee
from db.Task import Task

class HackersHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self, key=None):
        if key:
            # TODO: profile page
            # return self.write(id)
            userId = str(urllib.unquote(key))
            db_user = Attendee.search_database({'userId':key}).get()

            hacker = {}

            text_fields = [
                'nameFirst', 'nameLast', 'email', 'school',
                'year', 'userId'
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
            data['export_url'] = '/sponsor/export'
            hackers = self.get_hackers_memcache()
            data['hackers'] = [ hackers[i] for i in hackers ]
            data['num_people'] = len(data['hackers'])
            return self.render('sponsor/hackers.html', data=data, access=json.loads(self.db_user.access))

    def post(self, key=None):

        ids = json.loads(self.request.body)['ids']

        logging.info("Download Ids: %s" % str(ids))

        q = Attendee.query(ancestor=Attendee.get_default_event_parent_key())

        data = []
        for i in ids:
            hacker = q.filter(Attendee.userId == i).get()
            if not hacker:
                # TODO: error of some sort
                continue
            if not hacker.resume or (hacker.resume and not hacker.resume.gsObjectName):
                # hacker does not have a resume
                continue
            fileName = hacker.nameLast + '_' + hacker.nameFirst
            gsObjectName = hacker.resume.gsObjectName[17:]

            data.append({'fileName': fileName, 'gsObjectName': gsObjectName})

        t = Task(
            parent=Task.get_default_event_parent_key(),
            jobFunction='zip_resumes',
            data=data
        )

        t.put()

        logging.info("Download Task created")

        if not self.db_user.task_queue:
            self.db_user.task_queue = [t.key]
        else:
            self.db_user.task_queue.append(t.key)
        self.db_user.put()

        return self.write(json.dumps({"status": "success"}))
