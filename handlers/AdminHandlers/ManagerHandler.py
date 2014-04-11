import MainAdminHandler
from db.Admin import Admin
from db.Whitelist import Whitelist
from db import constants
from google.appengine.api import users

import urllib
import json
import re

class ManagerHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        data = {}

        db_admins = Admin.search_database({})
        data['admins'] = [ {'email':admin.email, 'access':json.loads(admin.access)} for admin in db_admins ]

        return self.render('admin_manager.html', data=data, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        emails = str(urllib.unquote(self.request.get('emails')))
        emails = emails.strip()
        emails = re.split(r'[,; \n]', emails)
        emails = [ email.strip() for email in emails ]
        valid_emails = []
        for email in emails:
            if re.match(constants.EMAIL_MATCH, email):
                valid_emails.append(email)

        # print valid_emails

        access = self.request.get_all('accessControl')

        allAccess = 'all' in access

        for email in valid_emails:
            db_user = Admin.search_database({'email': email}).get()
            if not db_user:
                Admin(
                    parent=Admin.get_default_event_parent_key(),
                    email=email,
                    googleUser=users.User(email),
                    statsAccess='stats' in access or allAccess,
                    approveAccess='approve' in access or allAccess,
                    approveAdminAccess='adminApprove' in access or allAccess,
                    mobileAccess='mobile' in access or allAccess,
                    corporateAdminAccess='corporate' in access or allAccess,
                    managerAccess='manager' in access or allAccess,
                    database_key=self.get_next_key()
                ).put()
            else:
                db_user.statsAccess = 'stats' in access or allAccess
                db_user.approveAccess = 'approve' in access or allAccess
                db_user.approveAdminAccess = 'adminApprove' in access or allAccess
                db_user.mobileAccess = 'mobile' in access or allAccess
                db_user.corporateAdminAccess = 'corporate' in access or allAccess
                db_user.managerAccess = 'manager' in access or allAccess
                db_user.put()

        return self.redirect('/admin/manager')
