import MainHandler
import re
from datetime import datetime
from db.Attendee import Attendee
from db.SignUp import SignUp
import logging
from google.appengine.api import users

email_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
from db.Attendee import Attendee
from google.appengine.api import users

class IndexHandler(MainHandler.Handler):
    ## Handler for the homepage
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

        buttonText = 'Apply'
        addedClassesForLoggedInUsers = ''

        user = users.get_current_user()
        
        if user:
            db_user = Attendee.search_database({'userId': user.user_id()}).get()
            if db_user and db_user.isRegistered:
                buttonText = 'Update Profile'
                addedClassesForLoggedInUsers = 'update-btn' 
                # Above line adds classes for fixing button size if person is updating application. Sorry about the long but descriptive var name.

        self.render("index.html", buttonText=buttonText, addedClassesForLoggedInUsers=addedClassesForLoggedInUsers)
