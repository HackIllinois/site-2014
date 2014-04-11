import MainHandler
from db import constants

class IndexHandler(MainHandler.Handler):
    def get(self):
        self.render("index.html", sponsorLogos=constants.SPONSOR_LOGOS)
