from handlers import MainHandler
from db.CorporateUrl import CorporateUrl
from db.Sponsor import Sponsor
from google.appengine.api import users

class RegistrationHandler(MainHandler.Handler):
    def get(self, key):
        if not key:
            return self.redirect('/corporate/invalidurl')

        key = str(key)

        db_url = CorporateUrl.search_database({'uniqueString': key}).get()
        if not db_url:
            return self.redirect('/corporate/invalidurl')

        if db_url.enabled == False:
            return self.redirect('/corporate/urlalreadyused')

        google_user = users.get_current_user()
        if google_user:
            db_user = Sponsor.search_database({'userId': google_user.user_id()}).get()
            if db_user:
                if db_user.attendeeDataAccess == False:
                    db_user.attendeeDataAccess = db_url.attendeeDataAccess
                    db_user.put()
                if db_user.attendeeDataAccess == False:
                    return self.redirect('/corporate')
                else:
                    return self.redirect('/corporate/hackers')

        data = {}
        data['redirectUrl'] = '/corporate/register/' + key
        return self.render('sponsor/registration.html', data=data)
