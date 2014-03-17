import logging

import MainHandler

from db.Attendee import Attendee
from db import constants
from google.appengine.api import users


class RsvpHandler(MainHandler.Handler):
    def get(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')
        db_user = Attendee.search_database({'userId': user.user_id()}).get()
        data = {}
        data['title'] = "RSVP"
        self.render("rsvp.html", data=data)

    def post(self):
        pass