import MainSponsorHandler
import urllib, logging, json
from db.Sponsor import Sponsor
from db import constants

class EditProfileHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        corporate_user = self.get_sponsor_user()
        if not corporate_user: return self.abort(500, detail='User not in database')

        data = {}
        text_fields = ['email', 'companyName', 'name', 'userEmail']

        for field in text_fields:
            value = getattr(corporate_user, field) # Gets db_user.field using a string
            if value is not None: data[field] = value

        return self.render("sponsor/edit_profile.html", data=data, access=json.loads(self.db_user.access))
	
    def post(self):

        corporate_user = self.get_sponsor_user()
        if not corporate_user: return self.abort(500, detail='User not in database')

        name = str(urllib.unquote(self.request.get('name')))
        companyName = str(urllib.unquote(self.request.get('companyName')))
        email = str(urllib.unquote(self.request.get('email')))
		
        corporate_user.name = name
        corporate_user.companyName = companyName
        corporate_user.email = email

        corporate_user.put()
		

        return 'agf'