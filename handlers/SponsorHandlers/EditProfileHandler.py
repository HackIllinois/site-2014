import MainSponsorHandler
import urllib, logging, json
from db.Sponsor import Sponsor
from db import constants

class EditProfileHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        data = {}
        text_fields = ['email', 'companyName', 'name', 'userEmail', 'jobTitle']

        for field in text_fields:
            value = getattr(self.db_user, field) # Gets db_user.field using a string
            if value is not None: data[field] = value

        return self.render("sponsor/edit_profile.html", data=data, access=json.loads(self.db_user.access))

    def post(self):
        self.db_user = self.get_sponsor_user()
        if not self.db_user: return self.abort(500, detail='User not in database')

        name = str(urllib.unquote(self.request.get('name')))
        companyName = str(urllib.unquote(self.request.get('companyName')))
        email = str(urllib.unquote(self.request.get('email')))
        jobTitle = str(urllib.unquote(self.request.get('jobTitle')))

        self.db_user.name = name
        self.db_user.companyName = companyName
        self.db_user.email = email
        self.db_user.jobTitle = jobTitle

        self.db_user.put()

        return self.write("success")
