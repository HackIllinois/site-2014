import MainHandler
from google.appengine.api import urlfetch
from google.appengine.api import users
from db.Admin import Admin
from db.constants import TEST_SITE_URLS as all_extensions
#ignore
from db.Task import Task

def get_admin_user():
    user = users.get_current_user()
    if not user: return None
    admin_user = Admin.search_database({'email': user.email()}).get()
    if not admin_user: return None
    return admin_user


class TestAllHandler(MainHandler.BaseAdminHandler):

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
        # Super hacky way to populate the database in a low impact page -- ignore, will be removed almost instantly
        newTask = {}
        newTask['jobFunction'] = 'zip_resumes'
        newTask['data'] = [['gsObjectName'='/gs/hackillinois/L2FwcGhvc3RpbmdfcHJvZC9ibG9icy9BRW5CMlVvOXlyeXVPTlRnRi0wbkkxVnRJZzdOQWd1dEw3cmVEcjBSOXMyRGowTEo4OU9tejZoYU5DMEFWUkNTVzNnZEJqYWFRYlBBMkJneGF4akF3TXNZT0JzMmJpZXRjZy40OEFGZnlKM21Rd2VxcDZa'],['gsObjectName'='/gs/hackillinois/L2FwcGhvc3RpbmdfcHJvZC9ibG9icy9BRW5CMlVxQmwzYmxnMFZoYXhPRjh6Rm1GblJ5RnJVRXlYUE5OcTZ3ank4R240YjJwbVdraGlUMDNiQTh5RFlwTDk2VnFYc3RaUUNaV2VjcEIyV0lRTGF3d0JnMGRyNG9Fdy5jNDZWUk9jMmZHUHY1VlhQ']]
        Task.add(newTask)
        
        # This will test the correct website: I.E. if you are running locally,
        # BASE_URL will be http://localhost:8080
        BASE_URL = self.request.application_url

        self.write("<h3>Test all URLs at " + BASE_URL + "</h3>")
        self.write('<table border="1" cellpadding="5">')
        for extension in all_extensions:
            self.test_index(BASE_URL, extension)
        self.write('</table>')


class TestAllJsHandler(MainHandler.BaseAdminHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.fullAccess:
            return self.abort(401, detail='User does not have permission to run tests.')

        data = {}
        data['base'] = self.request.application_url
        data['extensions'] = all_extensions
        return self.render('tests.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)