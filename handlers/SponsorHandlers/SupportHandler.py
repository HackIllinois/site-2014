import MainSponsorHandler
from db import constants
import json

class SupportHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        data = {}
        return self.render('sponsor/support.html', data=data, access=json.loads(self.db_user.access))
