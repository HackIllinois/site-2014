from AdminHandlers import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db.Status import Status
from db import constants
from google.appengine.api import memcache
import logging
from datetime import datetime

class CheckInHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, status=None, category=None, route=None):
        data = {}
        data['hackers'] = self.get_hackers_better_memcache(status, category, route)

        return self.render("checkin.html", data=data)

    def post(self):
        userId = str(urllib.unquote(self.request.get('userId')))
        number = str(urllib.unquote(self.request.get('number')))
        notes = str(urllib.unquote(self.request.get('notes')))

        db_user = Attendee.search_database({'userId':userId}).get()

        if not db_user:
            return logging.error("Attendee not in Database")

        db_user.notes = notes
        db_user.phoneNumber = number
        db_user.isCheckedIn = False
        db_user.checkInTime = datetime.now()

        db_user.put()

        return self.write('success')
