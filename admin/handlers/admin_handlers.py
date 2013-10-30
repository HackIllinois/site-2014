import sys
sys.path.append("../..")

import MainHandler
from db import db
from db import models

class AdminHandler(MainHandler.Handler):
    def get(self):
        self.response.write('Hello Admin!')

handlers = [('/admin', AdminHandler)]