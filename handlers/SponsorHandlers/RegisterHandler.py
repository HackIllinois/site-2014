from handlers import MainHandler
from google.appengine.api import users
from db.Sponsor import Sponsor
from db.CorporateUrl import CorporateUrl
from db import constants
import random
import urllib
from datetime import datetime

class RegisterHandler(MainHandler.Handler):
    def check_user_and_key(self, key):
        google_user = users.get_current_user()
        if not google_user:
            self.abort(500, detail='User not logged in')
            return None

        if not key:
            self.redirect('/corporate/invalidurl')
            return None

        key = str(key)

        db_url = CorporateUrl.search_database({'uniqueString': key}).get()

        if not db_url:
            self.redirect('/corporate/invalidurl')
            return None

        if db_url.enabled == False:
            self.redirect('/corporate/urlalreadyused')
            return None

        db_user = Sponsor.search_database({'userId': google_user.user_id()}).get()
        if db_user:
            if db_user.attendeeDataAccess == False:
                db_user.attendeeDataAccess = db_url.attendeeDataAccess
                db_user.put()
            if db_user.attendeeDataAccess == False:
                self.redirect('/corporate')
            else:
                self.redirect('/corporate/hackers')
            return None

        return google_user, db_url

    def get_next_key(self):
        key = None
        while not key:
            i = random.randint(constants.SPONSOR_START_COUNT, constants.SPONSOR_START_COUNT+9998)
            c = Sponsor.query(Sponsor.database_key == i).count()
            if c == 0: key = i
        return key

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
            attendeeDataAccess=db_url.attendeeDataAccess,
            database_key=self.get_next_key()
        ).put()

        if db_url.uniqueString not in constants.ALWAYS_ENABLED_URLS:
            db_url.enabled = False
            db_url.googleUser = google_user
            db_url.registerTime = datetime.now()
            db_url.put()

        if db_url.attendeeDataAccess == False:
            return self.redirect('/corporate')
        else:
            return self.redirect('/corporate/hackers')
