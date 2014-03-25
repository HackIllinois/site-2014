import MainAdminHandler
from db import constants

class IndexHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = {}
        data['registerCount'] = self.get_apply_count_memcache(constants.USE_ADMIN_MEMCACHE)
        data['schoolCount'] = self.get_school_count_memcache(constants.USE_ADMIN_MEMCACHE)
        data['approveCount'] = self.get_approve_count_memcache(constants.USE_ADMIN_MEMCACHE)
        # data['waitlistCount'] = self.get_waitlist_count_memcache(constants.USE_ADMIN_MEMCACHE)
        # data['emailedCount'] = self.get_emailed_count_memcache(constants.USE_ADMIN_MEMCACHE)
        # data['rsvpYesCount'] = self.get_rsvp_yes_count_memcache(constants.USE_ADMIN_MEMCACHE)
        # data['rsvpNoCount'] = self.get_rsvp_no_count_memcache(constants.USE_ADMIN_MEMCACHE)
        data['waitlistCount'] = 0
        data['emailedCount'] = 0
        data['rsvpYesCount'] = 0
        data['rsvpNoCount'] = 0

        return self.render('admin.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)
