import MainAdminHandler
from google.appengine.api import urlfetch
from google.appengine.api import users
from db.Admin import Admin
from db.constants import TEST_SITE_URLS as all_extensions

class TestAllHandler(MainAdminHandler.BaseAdminHandler):

    def test_index(self, base, extension):

        url = base + extension

        result = urlfetch.fetch(url)
        self.write('<tr><td>' + extension + '</td>')
        if result.status_code == 200:
            self.write('<td>yay :)</td>')
        else:
            self.write('<td>boo :(</td>')

        self.write('</tr>')


    def get(self):
        # This will test the correct website: I.E. if you are running locally,
        # BASE_URL will be http://localhost:8080
        BASE_URL = self.request.application_url

        self.write("<h3>Test all URLs at " + BASE_URL + "</h3>")
        self.write('<table border="1" cellpadding="5">')
        for extension in all_extensions:
            self.test_index(BASE_URL, extension)
        self.write('</table>')


class TestAllJsHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.fullAccess:
            return self.abort(401, detail='User does not have permission to run tests.')

        data = {}
        data['base'] = self.request.application_url
        data['extensions'] = all_extensions
        return self.render('tests.html', data=data, approveAccess=admin_user.approveAccess, mobileAccess=admin_user.mobileAccess, fullAccess=admin_user.fullAccess)