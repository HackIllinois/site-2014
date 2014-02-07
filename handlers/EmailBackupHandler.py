import MainHandler

from datetime import datetime
import json
import logging

from db.SignUp import SignUp

from google.appengine.api import mail

class EmailBackupHandler(MainHandler.Handler):
    """ Endpoint for email backups of the database. """
    def get(self):
        if True or "X-Appengine-Cron" in self.request.headers:

            emails = []

            q = SignUp.query()
            for e in q:
                emails.append(e.email)

            body_str = json.dumps(emails)
            logging.info(body_str)

            mail.send_mail(sender="rob@hackillinois.org",
                           to="db-backup@hackillinois.org",
                           subject="Email Backup: "+str(datetime.now().date()),
                           body=body_str)

        self.redirect("/")
