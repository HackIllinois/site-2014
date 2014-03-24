import MainAdminHandler
import urllib
from db import constants

class ApproveSchoolHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, school):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        school = str(urllib.unquote(school))

        data = {}
        data['hackers'] = []
        hackers = self.get_hackers_memecache(constants.USE_ADMIN_MEMCACHE)
        for h in hackers:
            if h['school'] == school:
                data['hackers'].append(h)

        # self.render("approve.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)
        self.render("summary.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)