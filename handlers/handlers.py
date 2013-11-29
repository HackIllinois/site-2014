import sys
# sys.path.append("../..")

import MainHandler
import datetime
import logging
import re
import json

from db import db
from db import models
from db.models import SignUp
from google.appengine.ext import db
from google.appengine.api import mail

email_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

class IndexHandler(MainHandler.Handler):
    """ Handler for the homepage """
    def get(self):
        self.render("index.html")

    def post(self):

        email = self.request.body

        if re.match(email_regex, email):
            today = datetime.datetime.now().date()

            newSignup = SignUp(email=email)
            newSignup.register_date = today
            newSignup.put()

            logging.info('Signup with email %s', email)


class ErrorHandler(MainHandler.Handler):
    """ 404 Handler """
    def get(self):
        self.redirect("/")

class EmailBackupHandler(MainHandler.Handler):
    """ Endpoint for email backups of the database. """
    def get(self):
        if "X-Appengine-Cron" in self.request.headers:

            emails = []

            q = SignUp.all()
            for e in q:
                emails.append(e.email)

            body_str = json.dumps(emails)
            logging.info(body_str)

            mail.send_mail(sender="rob@hackillinois.org",
                           to="db-backup@hackillinois.org",
                           subject="Email Backup: "+str(datetime.datetime.now().date()),
                           body=body_str)

        self.redirect("/")

handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('.*', ErrorHandler)
]