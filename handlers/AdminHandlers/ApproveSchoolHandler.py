import MainAdminHandler
import urllib
from db import constants
import json

class ApproveSchoolHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, school):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        school = str(urllib.unquote(school))

        data = {}
        data['hackers'] = []
        hackers = self.get_hackers_memcache(constants.USE_ADMIN_MEMCACHE)
        for h in hackers:
            if h['school'] == school:
                data['hackers'].append(h)

        self.render("summary.html", data=data, access=json.loads(admin_user.access))