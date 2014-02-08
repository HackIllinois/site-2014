import MainHandler
import re
from datetime import datetime
from db.Attendee import Attendee
from db.SignUp import SignUp
import logging
from google.appengine.api import users

email_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

class IndexHandler(MainHandler.Handler):
    """ Handler for the homepage, """
    def get(self):
    
        data = {}
        user = users.get_current_user()
        data['isLoggedIn'] = False
        if user is not None:
            db_user = Attendee.search_database({'userId': user.user_id()}).get()
            if db_user is not None and db_user.isRegistered:
                  data['isLoggedIn'] = True
    
        self.render("index.html", data=data)

    def post(self):
        """ Handle email signups """
        email = self.request.body

        if re.match(email_regex, email):
            today = datetime.now().date()

            newSignup = SignUp(email=email)
            newSignup.register_date = today
            newSignup.put()

            logging.info('Signup with email %s', email)
