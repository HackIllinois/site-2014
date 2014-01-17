import MainHandler
from db.models import SignUp

class SignupCountHandler(MainHandler.Handler):
    """ Handler for a quick page to count the number of email signups we have """
    def get(self):
        num_signups = SignUp.query().count()
        self.write(num_signups)
