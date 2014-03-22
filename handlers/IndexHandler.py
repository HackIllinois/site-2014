import MainHandler
import re
from datetime import datetime
from db.Attendee import Attendee
from db.SignUp import SignUp
import logging
from google.appengine.api import users

from db.Attendee import Attendee
from google.appengine.api import users

class IndexHandler(MainHandler.Handler):
    def get(self):
        data = {}
        self.render("index.html", data=data)
