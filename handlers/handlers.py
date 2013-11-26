import sys
sys.path.append("../..")

import MainHandler
import datetime
import logging
import re
import json

from db import db
from db import models
from google.appengine.ext import db
from google.appengine.api import mail

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

class EmailBackupHandler(MainHandler.Handler):
    def get(self):
        if "X-Appengine-Cron" in self.request.headers:
        
            emails = []
        
            q = SignUp.all()
            for e in q:
                emails.append(e.email)

            body_str = json.dumps(emails)
            logging.info(body_str)

            mail.send_mail(sender="db-backup@hackillinois.org",
                           to="db-backup@hackillinois.org",
                           subject="Email Backup: "+str(datetime.datetime.now().date()),
                           body=body_str)

        self.redirect("/")

handlers = [('/', IndexHandler),('/emailbackup',EmailBackupHandler),('.*', ErrorHandler)]