import MainSponsorHandler
from db import constants
import json

class EditProfileHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        data = {}
        return self.render('sponsor/edit_profile.html', data=data, access=json.loads(self.db_user.access))
