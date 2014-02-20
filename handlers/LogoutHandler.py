import MainHandler
import urllib
from google.appengine.api import users

class LogoutHandler(MainHandler.Handler):
    def get(self):
        redirUrl = str(urllib.unquote(self.request.get('redirect')))
        redirUrl = redirUrl if redirUrl else '/'

        user = users.get_current_user()
        if not user: return self.redirect(redirUrl)

        url = users.create_logout_url(redirUrl)
        return self.redirect(url)
