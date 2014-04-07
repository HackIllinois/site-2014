import MainSponsorHandler
from db import constants
import json

class HackersHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        me = self.db_user

        data = {}
        return self.render('sponsor/hackers.html', data=data, access=json.loads(self.db_user.access))
