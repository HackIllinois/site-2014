import MainSponsorHandler
import urllib, logging, json
from db.Sponsor import Sponsor
from db import constants

class ProfileHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        data = {}
        text_fields = ['email', 'companyName', 'name', 'userEmail', 'jobTitle']

        for field in text_fields:
            value = getattr(self.db_user, field) # Gets db_user.field using a string
            if value is not None: data[field] = value

        return self.render("sponsor/profile.html", data=data, access=json.loads(self.db_user.access))
