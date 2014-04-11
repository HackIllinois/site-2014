import MainAdminHandler
import urllib, logging, json
from db.Admin import Admin
from db import constants

class EditMyProfileHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = {}
        text_fields = ['email', 'companyName', 'name', 'userEmail', 'jobTitle']

        for field in text_fields:
            value = getattr(self.db_user, field) # Gets db_user.field using a string
            if value is not None: data[field] = value

        return self.render('admin_edit_my_profile.html', data=data, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

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
