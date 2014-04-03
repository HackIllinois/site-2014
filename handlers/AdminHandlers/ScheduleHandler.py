import MainAdminHandler

class ScheduleHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')

        data = {}
        return self.render("admin_mobile_schedule.html", data=data, approveAccess=admin_user.approveAccess, mobileAccess=admin_user.mobileAccess, fullAccess=admin_user.fullAccess)

    def post(self):
        pass