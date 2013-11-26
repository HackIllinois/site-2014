import sys
sys.path.append("../..")

import MainHandler
import datetime
import logging
import re

from db import db
from db import models
from google.appengine.ext import db

email_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

class SignUp(db.Model):
    email = db.StringProperty(required=True)
    register_date = db.DateProperty()

class IndexHandler(MainHandler.Handler):
    def get(self):
        self.render("index.html")

    def post(self):
        
        email = self.request.get("register-email")
        if re.match(email_regex, email):
        
            today = datetime.datetime.now().date()
        
            newSignup = SignUp(email=email)
            newSignup.register_date = today
            newSignup.put()
        
            logging.info('Signup with email %s', email)
        
        self.redirect("/")

class ErrorHandler(MainHandler.Handler):
    def get(self):
        self.redirect("/")

handlers = [('/', IndexHandler),('.*', ErrorHandler)]