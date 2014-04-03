from AdminHandlers import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db.Status import Status
from db import constants
from google.appengine.api import memcache
import logging
from datetime import datetime

class CheckInHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, status=None, category=None, route=None):
        data = {}
        data['hackers'] = self.get_hackers_new_memecache(status, category, route, constants.USE_ADMIN_MEMCACHE)

        return self.render("checkin.html", data=data)