import MainHandler
from google.appengine.api import users

class AdminHandler(MainHandler.Handler):

    def get(self):
        user = users.get_current_user()
        if user:
            name = user.nickname()
        else:
            name = 'ERROR'
        self.render('admin.html', name=name)
