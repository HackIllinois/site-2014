import MainAdminHandler
from db import constants

class ApplyCountHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        cached_count = self.get_apply_count_memcache(constants.USE_ADMIN_MEMCACHE)
        return self.write('%d' % cached_count)