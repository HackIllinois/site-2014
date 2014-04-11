import MainSponsorHandler
from db import constants
import json

class IndexHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        data = {}
        return self.render('sponsor/index.html', data=data, access=json.loads(self.db_user.access))
