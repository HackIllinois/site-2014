import MainAdminHandler

class IndexHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        return self.render('admin.html', data={}, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)