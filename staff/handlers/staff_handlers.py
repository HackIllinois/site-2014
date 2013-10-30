import sys
sys.path.append("../..")

import MainHandler
from db import db
from db import models

class StaffHandler(MainHandler.Handler):
    def get(self):
        self.response.write('Hello Staff!')

handlers = [('/staff', StaffHandler)]