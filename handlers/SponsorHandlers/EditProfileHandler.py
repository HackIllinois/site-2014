import MainSponsorHandler
from db import constants
import json

class EditProfileHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        me = self.db_user

        data = {}
        # return self.render('admin.html', data=data, access=json.loads(admin_user.access))
        return self.render('sponsor/edit_profile.html', data=data, access=json.loads(self.db_user.access))
