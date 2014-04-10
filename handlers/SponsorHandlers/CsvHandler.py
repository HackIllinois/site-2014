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

class CsvHandler(MainSponsorHandler.BaseSponsorHandler):
    def post(self):
        if not self.request.body:
            return self.abort(500, detail="No request body")

        data_in = json.loads(self.request.get('data'))
        data_all = data_in['all']
        data_ids = data_in['ids'] if 'ids' in data_in else None

        logging.info("Download All: %s" % str(data_all))
        if data_all: logging.info("Download Ids: %s" % str(data_ids))

        if data_all:
            hackers = self.get_hackers_memcache(True)
            output = cStringIO.StringIO()
            writer = csv.writer(output)
            base_url = self.request.application_url

            fields = ['nameFirst','nameLast','email','school','year']
            csv_headings = ['First Name','Last Name','Email','School','Year', 'Resume']

            writer.writerow(csv_headings)
            for i in hackers:
                hacker = hackers[i]

                row = []
                for f in fields:
                    if f in hacker and hacker[f] is not None:
                        row.append(hacker[f])
                    else:
                        row.append('')

                if hacker['hasResume']:
                    row.append(base_url + '/corporate/resume?userId='+hacker['userId'])
                else:
                    row.append('')

                writer.writerow(row)

            csv_string = output.getvalue()
            output.close()

        else:
            hackers = self.get_hackers_memcache(True)
            output = cStringIO.StringIO()
            writer = csv.writer(output)
            base_url = self.request.application_url

            fields = ['nameFirst','nameLast','email','school','year']
            csv_headings = ['First Name','Last Name','Email','School','Year', 'Resume']

            writer.writerow(csv_headings)
            for i in data_ids:
                if i not in hackers:
                    # TODO: error of some sort
                    continue

                hacker = hackers[i]

                if not hacker:
                    # TODO: error of some sort
                    continue

                row = []
                for f in fields:
                    if f in hacker and hacker[f] is not None:
                        row.append(hacker[f])
                    else:
                        row.append('')

                if hacker['hasResume']:
                    row.append(base_url + '/corporate/resume?userId='+hacker['userId'])
                else:
                    row.append('')

                writer.writerow(row)

            csv_string = output.getvalue()
            output.close()

        dt = datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment;filename=HackIllinois-' + dt + '.csv'
        return self.write(csv_string)
