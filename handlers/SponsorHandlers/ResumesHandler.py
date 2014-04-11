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

class ResumesHandler(MainSponsorHandler.BaseSponsorHandler):
    def post(self):
        if not self.request.body:
            return self.abort(500, detail="No request body")

        data_in = json.loads(self.request.get('data'))
        data_all = data_in['all']
        data_ids = data_in['ids'] if 'ids' in data_in else None

        logging.info("Download All: %s" % str(data_all))
        if not data_all: logging.info("Download Ids: %s" % str(data_ids))

        if data_all:
            hackers = self.get_hackers_memcache(True)

            data = []
            for i in hackers:
                hacker = hackers[i]

                if not hacker['resumeLocation']:
                    # TODO: error of some sort
                    # hacker does not have a resume
                    continue

                fileName = hacker['nameLast'] + '_' + hacker['nameFirst']
                gsObjectName = hacker['resumeLocation']

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

        else:
            hackers = self.get_hackers_memcache(True)

            data = []
            for i in data_ids:
                if i not in hackers:
                    # TODO: error of some sort
                    continue

                hacker = hackers[i]

                if not hacker:
                    # TODO: error of some sort
                    continue
                if not hacker['resumeLocation']:
                    # TODO: error of some sort
                    # hacker does not have a resume
                    continue

                fileName = hacker['nameLast'] + '_' + hacker['nameFirst']
                gsObjectName = hacker['resumeLocation']

                data.append({'fileName': fileName, 'gsObjectName': gsObjectName})

            if not data:
                return self.abort(500, detail="No hackers selected")

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

        # return self.write(json.dumps({"status": "success"}))
        return self.redirect('/corporate/queue')
