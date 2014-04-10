from handlers import MainHandler
from db.CorporateUrl import CorporateUrl

class RegistrationHandler(MainHandler.Handler):
    def get(self, key):
        # 1. Check if key is in database
            # No: Give error page
            # Yes: Goto 2
        # 2. Check if key is enabled
            # No: Give error page
            # Yes: Goto 3
        # 3. Render page explaining that we will be using their google account as a login so we do not have to store their password
        # 4. Button that confirms they understand and redirects to /corporate/register/<key>

        if not key:
            return self.redirect('/corporate/invalidurl')

        key = str(key)

        db_url = CorporateUrl.search_database({'uniqueString': key}).get()
        if not db_url:
            return self.redirect('/corporate/invalidurl')

        if db_url.enabled == False:
            return self.redirect('/corporate/urlalreadyused')

        data = {}
        data['redirectUrl'] = '/corporate/register/' + key
        return self.render('sponsor/registration.html', data=data)
