import MainHandler
from google.appengine.api import urlfetch
from db.constants import TEST_SITE_URLS as all_extensions

class TestAllHandlers(MainHandler.BaseAdminHandler):

    def test_index(self, extension):

        url = 'http://dev.hackillinois.org' + extension # TODO: parameter to test dev, master, etc.
        
        result = urlfetch.fetch(url)
        self.write('<tr><td>' + extension + '</td>')
        if result.status_code == 200:
            self.write('<td>yay :)</td>')
        else:
            self.write('<td>boo :(</td>')

        self.write('</tr>')


    def get(self):
        self.write("<h3>Test all URLs at http://dev.hackillinois.org/</h3>")
        self.write('<table border="1" cellpadding="5">')
        for extension in all_extensions:
            self.test_index(extension)
        self.write('</table>')