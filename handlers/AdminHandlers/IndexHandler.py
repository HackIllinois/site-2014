import MainAdminHandler
from db import constants
import json

class IndexHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = {}
        data['registerCount'] = self.get_apply_count_memcache(constants.USE_ADMIN_MEMCACHE)
        data['schoolCount'] = self.get_school_count_memcache(constants.USE_ADMIN_MEMCACHE)
        data['approveCount'] = self.get_status_count_memcache('Approved', constants.USE_ADMIN_MEMCACHE)
        data['waitlistCount'] = self.get_status_count_memcache('Waitlisted', constants.USE_ADMIN_MEMCACHE)
        data['emailedCount'] = self.get_status_count_memcache('Awaiting Response', constants.USE_ADMIN_MEMCACHE)
        data['rsvpYesCount'] = self.get_status_count_memcache('Rsvp Coming', constants.USE_ADMIN_MEMCACHE)
        data['rsvpNoCount'] = self.get_status_count_memcache('Rsvp Not Coming', constants.USE_ADMIN_MEMCACHE)
        data['rsvpInvalidCount'] = self.get_status_count_memcache('No Rsvp', constants.USE_ADMIN_MEMCACHE)

        return self.render('admin.html', data=data, access=json.loads(admin_user.access))
