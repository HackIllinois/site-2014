from handlers import MainHandler
from google.appengine.api import users
from db.Sponsor import Sponsor
from db.CorporateUrl import CorporateUrl
import urllib
from datetime import datetime

class RegisterHandler(MainHandler.Handler):
    def check_user_and_key(self, key):
        google_user = users.get_current_user()
        if not google_user:
            self.abort(500, detail='User not logged in')
            return None

        # If user is already in database, redirect to /corporate
        db_user = Sponsor.search_database({'userId': google_user.user_id()}).get()
        if db_user:
            self.redirect('/corporate')
            return None

        if not key:
            # TODO: Error page
            self.write('URL Not Valid')
            return None

        key = str(key)

        db_url = CorporateUrl.search_database({'uniqueString': key}).get()
        if not db_url:
            # TODO: Error page
            self.write('URL Not Valid')
            return None

        if db_url.enabled == False:
            # TODO: Error page
            self.write('URL Already Used')
            return None

        return google_user, db_url

    def get(self, key):
        ret = self.check_user_and_key(key)
        if not ret: return
        google_user, db_url = ret

        data = {}
        data['email'] = google_user.email()
        data['logoutUrl'] = '/logout?redirect=' + urllib.quote(self.request.url)

        return self.render('sponsor/register.html', data=data)

    def post(self, key):
        ret = self.check_user_and_key(key)
        if not ret: return
        google_user, db_url = ret

        Sponsor(
            parent=Sponsor.get_default_event_parent_key(),
            googleUser=google_user,
            attendeeDataAccess=db_url.attendeeDataAccess
        ).put()

        db_url.enabled = False
        db_url.googleUser = google_user
        db_url.registerTime = datetime.now()
        db_url.put()

        return self.redirect("/corporate")
