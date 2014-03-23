import MainAdminHandler
from db.Admin import Admin

import urllib

class AccessControlHandler(MainAdminHandler.BaseAdminHandler):
    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.fullAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        email = str(urllib.unquote(self.request.get('email')))
        accessControl = self.request.get('accessControl')
        approveAccess = accessControl == 'approve'
        fullAccess = accessControl == 'full'

        db_user = Admin.search_database({'email': email}).get()
        if not db_user:
            Admin.add({'approveAccess':(approveAccess or fullAccess),
                       'fullAccess':fullAccess,
                       'email': email})
        else:
            Admin.update_search({'approveAccess':(approveAccess or fullAccess),
                                 'fullAccess':fullAccess},
                                {'email': email})

        return self.redirect('/admin/manager')