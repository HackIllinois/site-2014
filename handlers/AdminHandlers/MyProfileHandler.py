import MainAdminHandler
import urllib, logging, json
from db.Admin import Admin
from db import constants

class MyProfileHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = {}
        text_fields = ['email', 'companyName', 'name', 'userEmail', 'jobTitle']

        for field in text_fields:
            value = getattr(self.db_user, field) # Gets db_user.field using a string
            if value is not None: data[field] = value

        return self.render('admin_my_profile.html', data=data, access=json.loads(admin_user.access))
