import sys
sys.path.append("../..")

import MainHandler
from db import db
from db import models

class SponsorHandler(MainHandler.Handler):
    def get(self):
        self.response.write('Hello Sponsors!')

handlers = [('/sponsor', SponsorHandler)]