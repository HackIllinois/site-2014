import MainHandler
from google.appengine.api import urlfetch
from db.constants import TEST_SITE_URLS as all_extensions

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
        data = {}
        data['base'] = self.request.application_url
        data['extensions'] = all_extensions
        return self.render('tests.html', data=data)