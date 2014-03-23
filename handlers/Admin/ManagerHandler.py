import MainAdminHandler
from db.Admin import Admin

class ManagerHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        db_admins = Admin.search_database({})
        admins = [ {'email':admin.email, 'approveAccess':admin.approveAccess, 'fullAccess':admin.fullAccess} for admin in db_admins ]
        data = {'admins':admins}
        return self.render('admin_manager.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)
