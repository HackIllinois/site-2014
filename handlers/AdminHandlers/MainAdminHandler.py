import logging
import csv
import cStringIO

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from handlers import MainHandler
from db import constants
from db.Attendee import Attendee
from db.Admin import Admin

class BaseAdminHandler(MainHandler.Handler):
    """
    This is for all /admin pages
    Overrides the dispatch method (called before get/post/etc.)
    Sends 401 (Unauthorized) if user is not an admin
    Ref: http://webapp-improved.appspot.com/guide/handlers.html
    """
    def dispatch(self):
        is_admin = False

        user = users.get_current_user()
        if not user:
            return self.abort(401)

        email = user.email()
        domain = email.split('@')[1] if len(email.split('@')) == 2 else None # Sanity check

        admin_user = Admin.search_database({'email': user.email()}).get()
        if admin_user:
            is_admin = True
        elif email in constants.ADMIN_EMAILS:
            parent = Admin.get_default_event_parent_key()
            Admin(parent=parent, email=user.email(), googleUser=user, approveAccess=True, fullAccess=True).put()
            is_admin = True
        elif domain == 'hackillinois.org':
            parent = Admin.get_default_event_parent_key()
            Admin(parent=parent, email=user.email(), googleUser=user).put()
            is_admin = True

        if is_admin:
            # Parent class will call the method to be dispatched
            # -- get() or post() or etc.
            logging.info('Admin user %s is online.', email)
            super(BaseAdminHandler, self).dispatch()
        else:
            logging.info('%s attempted to access an admin page but was denied.', email)
            return self.abort(401)

    def get_admin_user(self):
        """Returns the database Admin model for the current logged-in user"""
        user = users.get_current_user()
        if not user:
            return None
        admin_user = Admin.search_database({'email': user.email()}).get()
        if not admin_user:
            return None
        return admin_user

    def get_hackers_memecache(self, use_memcache=False):
        """Gets the 'hackers' key from the memcache and updates the memcache if the key is not in the memcache"""
        data = memcache.get('hackers')
        if data is None or not use_memcache:
            data = self.set_hackers_memcache()
        return data

    def get_apply_count_memcache(self, use_memcache=False):
        """Gets the 'apply_count' key from memcache"""
        cached_count = memcache.get('apply_count')
        if cached_count is None or not use_memcache:
            cached_count = self.set_apply_count_memcache()
        return cached_count

    def get_approve_count_memcache(self, use_memcache=False):
        """Gets the 'approve_count' key from memcache"""
        cached_count = memcache.get('approve_count')
        if cached_count is None or not use_memcache:
            cached_count = self.set_approve_count_memcache()
        return cached_count

    def set_hackers_memcache(self):
        """Sets the 'hackers' key in the memcache"""
        hackers = Attendee.search_database({'isRegistered':True})
        data = []
        for hacker in hackers:
            data.append({ 'nameFirst':hacker.nameFirst,
                          'nameLast':hacker.nameLast,
                          'email':hacker.email,
                          'gender':hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                          'school':hacker.school,
                          'year':hacker.year,
                          'linkedin':hacker.linkedin,
                          'github':hacker.github,
                          'shirt':hacker.shirt,
                          'food':'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                          'projectType':hacker.projectType,
                          'resume':hacker.resume,
                          'registrationTime':hacker.registrationTime.strftime('%x %X'),
                          'isApproved':hacker.isApproved,
                          'userId':hacker.userId})

        if not memcache.add('hackers', data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return data

    def set_apply_count_memcache(self):
        """Sets the 'apply_count' key in memcache"""
        q = Attendee.query(Attendee.isRegistered == True)
        cached_count = q.count()
        if not memcache.add('apply_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return cached_count

    def set_approve_count_memcache(self):
        """Sets the 'approve_count' key in memcache"""
        q = Attendee.search_database({'isRegistered':True, 'isApproved':True})
        cached_count = q.count()
        if not memcache.add('approve_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return cached_count
