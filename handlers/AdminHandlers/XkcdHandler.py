import MainAdminHandler

from google.appengine.api import urlfetch

class XkcdHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        xkcd_json = urlfetch.fetch('http://xkcd.com/info.0.json').content
        self.response.headers.add("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'text/json'
        return self.write(xkcd_json)