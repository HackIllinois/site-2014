import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db import constants
from google.appengine.api import memcache
import logging
from datetime import datetime
from google.appengine.api import users

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
    def check_access(self):
        access_emails = ["checkin@hackillinois.org", "alex.burck@hackillinois.org"]
        user = users.get_current_user()
        if not user: return self.abort(401)
        email = user.email()
        if email not in access_emails: return self.abort(401)
        return True

    def get(self):
        if not self.check_access(): return

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
        if not self.check_access(): return

        userId = str(urllib.unquote(self.request.get('userId')))
        number = str(urllib.unquote(self.request.get('number')))
        notes = str(urllib.unquote(self.request.get('notes')))

        db_user = Attendee.search_database({'userId':userId}).get()

        if not db_user:
            logging.error("Attendee not in Database")
            self.write('Failure: Could not find user in database.')

        db_user.notes = notes
        db_user.phoneNumber = number
        db_user.isCheckedIn = True
        db_user.checkInTime = datetime.now()

        db_user.put()

        return self.write('Success')
