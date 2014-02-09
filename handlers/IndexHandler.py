import MainHandler
from db.Attendee import Attendee
from google.appengine.api import users

class IndexHandler(MainHandler.Handler):
    """ Handler for the homepage, """
    def get(self):
        buttonText = 'Apply'

        user = users.get_current_user()
        if user:
            db_user = Attendee.search_database({'userId': user.user_id()}).get()
            if db_user and db_user.isRegistered:
                buttonText = 'Update Profile'
                addedClassesForLoggedInUsers = 'update-btn' 
                # Above line adds classes for fixing button size if person is updating application. Sorry about the long but descriptive var name.

        self.render("index.html", buttonText=buttonText, addedClasses=addedClassesForLoggedInUsers)
