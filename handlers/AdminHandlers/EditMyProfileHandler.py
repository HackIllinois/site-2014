import MainAdminHandler
import urllib, logging, json
from db.Admin import Admin
from db import constants

class EditMyProfileHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        admin = {}
        text_fields = ['email', 'name', 'userEmail']

        for field in text_fields:
            value = getattr(admin_user, field) # Gets db_user.field using a string
            if value is not None: admin[field] = value

        return self.render('admin_edit_my_profile.html', admin=admin, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        name = str(urllib.unquote(self.request.get('name')))
        email = str(urllib.unquote(self.request.get('email')))

        admin_user.name = name
        admin_user.email = email

        admin_user.put()

        return self.write("success")
