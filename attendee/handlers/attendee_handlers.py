import sys
sys.path.append("../..")

import MainHandler
from db import db
from db import models

class AttendeeHandler(MainHandler.Handler):
    def get(self):
        self.response.write('Hello Everyone!')

handlers = [('/', AttendeeHandler)]