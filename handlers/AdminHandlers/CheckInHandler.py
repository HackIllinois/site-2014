import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db import constants
from google.appengine.api import memcache
import logging
from datetime import datetime

def serialize_hacker(hacker):
    return {
        'name': hacker.nameFirst + ' ' + hacker.nameLast,
        'email': hacker.email,
        'gender': hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
        'school': hacker.school,
        'shirt': hacker.shirt,
        'userId': hacker.userId,
    }


class CheckInHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        data = {}

        hackers = Attendee.query(
            Attendee.isRegistered == True,
            Attendee.approvalStatus.status == 'Rsvp Coming',
            Attendee.isCheckedIn == False,
            ancestor=Attendee.get_default_event_parent_key()
        )
        hackers = hackers.fetch(
            projection=[
                Attendee.nameFirst,
                Attendee.nameLast,
                Attendee.email,
                Attendee.gender,
                Attendee.school,
                Attendee.shirt,
                Attendee.userId,
            ]
        )
        data['hackers'] = [ serialize_hacker(h) for h in hackers ]

        return self.render("checkin.html", data=data)

    def post(self):
        """
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
        """
        return self.write('Not yet implemented')
