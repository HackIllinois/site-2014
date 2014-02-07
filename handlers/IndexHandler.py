import MainHandler
import re
from datetime import datetime
from db.SignUp import SignUp
import logging

email_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

class IndexHandler(MainHandler.Handler):
    """ Handler for the homepage, """
    def get(self):
        self.render("index.html")

    def post(self):
        """ Handle email signups """
        email = self.request.body

        if re.match(email_regex, email):
            today = datetime.now().date()

            newSignup = SignUp(email=email)
            newSignup.register_date = today
            newSignup.put()

            logging.info('Signup with email %s', email)
