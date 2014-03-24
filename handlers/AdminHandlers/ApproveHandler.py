import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db import constants

from google.appengine.api import memcache


class ApproveHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        data = {}
        data['hackers'] = self.get_hackers_memecache(constants.USE_ADMIN_MEMCACHE)

        # self.render("approve.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)
        # self.render("summary.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)
        self.render("admin_approve_base.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)

    def post(self):
        userId = str(urllib.unquote(self.request.get('userId')))
        user = Attendee.search_database({'userId':userId}).get()
        if not user:
            return self.abort(500, detail='User not in database')

        x = {}
        x['isApproved'] = str(self.request.get('isApproved')) == "True"
        success = Attendee.update_search(x, {'userId':userId})

        # Delete memcache key so /admin/approve is updated
        memcache.delete('hackers')

        return self.write(str(success))