import logging
import csv
import cStringIO
import random

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

    def __init__(self, request, response):
        super(BaseAdminHandler, self).__init__(request, response)

    def get_next_key(self):
        key = None
        while not key:
            i = random.randint(constants.ADMIN_START_COUNT, constants.ADMIN_START_COUNT+9998)
            c = Admin.search_database({'database_key':i}).count()
            if c == 0: key = i
        return key

    def dispatch(self):
        is_admin = False

        user = users.get_current_user()
        if not user:
            return self.abort(401)

        email = user.email()
        domain = email.split('@')[1] if len(email.split('@')) == 2 else None  # Sanity check

        admin_user = Admin.search_database({'email': user.email()}).get()
        if admin_user:
            is_admin = True
            if admin_user.userId is None or admin_user.userId == '':
                admin_user.userId = user.user_id()
                admin_user.put()
            if not admin_user.database_key:
                admin_user.database_key = self.get_next_key()
                admin_user.put()
        elif email in constants.ADMIN_EMAILS:
            parent = Admin.get_default_event_parent_key()
            Admin(parent=parent, email=user.email(), googleUser=user, userId=user.user_id(), approveAccess=True,
                  fullAccess=True, database_key=self.get_next_key()).put()
            is_admin = True
        elif domain == 'hackillinois.org':
            parent = Admin.get_default_event_parent_key()
            Admin(parent=parent, email=user.email(), googleUser=user, userId=user.user_id(), database_key=self.get_next_key()).put()
            is_admin = True

        if is_admin:
            # Parent class will call the method to be dispatched
            # -- get() or post() or etc.
            logging.info('Admin user %s is online.', email)
            super(BaseAdminHandler, self).dispatch()
        else:
            logging.info('%s attempted to access an admin page but was denied.', email)
            return self.abort(401)

    def require_and_get_admin_user(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        return admin_user


    def get_admin_user(self):
        """Returns the database Admin model for the current logged-in user"""
        user = users.get_current_user()
        if not user:
            return None
        admin_user = Admin.search_database({'email': user.email()}).get()
        if not admin_user:
            return None
        return admin_user

    def get_hackers_memcache(self, use_memcache=True):
        """Gets the 'hackers' key from the memcache and updates the memcache if the key is not in the memcache"""
        if use_memcache:
            data = memcache.get('hackers')
            if data is None:
                data = self.set_hackers_memcache()
            return data
        else:
            return self.set_hackers_memcache()

    def get_hackers_new_memcache(self, status=None, category=None, route=None, use_memcache=False):
        """Gets the 'hackers/<status>/<category>/<route>' key from the memcache and updates the memcache if the key is not in the memcache"""
        if use_memcache:
            key = 'hackers/' + str(status) + '/' + str(category) + '/' + str(route)
            data = memcache.get(key)
            if data is None: data = self.set_hackers_new_memcache(status, category, route)
            return data
        else:
            return self.set_hackers_new_memcache(status, category, route)

    def get_apply_count_memcache(self, use_memcache=True):
        """Gets the 'apply_count' key from memcache"""
        if use_memcache:
            cached_count = memcache.get('apply_count')
            if cached_count is None:
                cached_count = self.set_apply_count_memcache()
            return cached_count
        else:
            return self.set_apply_count_memcache()

    def get_school_count_memcache(self, use_memcache=True):
        """Gets the 'school_count' key from memcache"""
        if use_memcache:
            cached_count = memcache.get('school_count')
            if cached_count is None:
                cached_count = self.set_school_count_memcache()
            return cached_count
        else:
            return self.set_school_count_memcache()

    def get_approve_count_memcache(self, use_memcache=True):
        """Gets the 'approve_count' key from memcache"""
        if use_memcache:
            cached_count = memcache.get('approve_count')
            if cached_count is None:
                cached_count = self.set_approve_count_memcache()
            return cached_count
        else:
            return self.set_approve_count_memcache()

    def get_status_count_memcache(self, status, use_memcache=True):
        """Gets the 'status_count/<status>' key from memcache"""
        if use_memcache:
            cached_count = memcache.get('status_count/' + status)
            if cached_count is None:
                cached_count = self.set_status_count_memcache(status)
            return cached_count
        else:
            return self.set_status_count_memcache(status)

    def get_query_all_memcache(self, cls, model_type, use_memcache=True):
        if use_memcache:
            key = 'query_all/' + model_type
            data = memcache.get(key)
            if data is None:
                data = self.set_query_all_memcache(cls, model_type)
            return data
        else:
            return self.set_query_all_memcache(cls, model_type)

    def set_hackers_memcache(self):
        """Sets the 'hackers' key in the memcache"""
        hackers = Attendee.search_database({'isRegistered': True})
        data = []
        for hacker in hackers:
            data.append({'nameFirst': hacker.nameFirst,
                         'nameLast': hacker.nameLast,
                         'email': hacker.email,
                         'gender': hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                         'school': hacker.school,
                         'year': hacker.year,
                         'linkedin': hacker.linkedin,
                         'github': hacker.github,
                         'shirt': hacker.shirt,
                         'food': 'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                         'projectType': hacker.projectType,
                         'resume': hacker.resume,
                         'registrationTime': hacker.registrationTime.strftime('%x %X'),
                         'isApproved': hacker.isApproved,
                         'userId': hacker.userId})

        if not memcache.set('hackers', data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return data

    def set_hackers_new_memcache(self, status=None, category=None, route=None):
        """Sets the 'hackers/<status>/<category>/<route>' key in the memcache"""
        key = 'hackers/' + str(status) + '/' + str(category) + '/' + str(route)
        hackers = None

        # Change search of category='I have not responded to this quesiton' to ''
        category = '' if category == 'I have not responded to this quesiton' else category

        if status is not None and status != 'a' and status != 'b' and status != 'All':
            if category is not None:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status,
                                             Attendee.travel == category, Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status,
                                             Attendee.travel == category,
                                             ancestor=Attendee.get_default_event_parent_key())
            else:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status,
                                             Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status,
                                             ancestor=Attendee.get_default_event_parent_key())
        elif status == 'a':
            if category is not None:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.APPROVE_STATUSES),
                                             Attendee.travel == category, Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.APPROVE_STATUSES),
                                             Attendee.travel == category,
                                             ancestor=Attendee.get_default_event_parent_key())
            else:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.APPROVE_STATUSES),
                                             Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.APPROVE_STATUSES),
                                             ancestor=Attendee.get_default_event_parent_key())
        elif status == 'b':
            if category is not None:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.RSVP_STATUSES),
                                             Attendee.travel == category, Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.RSVP_STATUSES),
                                             Attendee.travel == category,
                                             ancestor=Attendee.get_default_event_parent_key())
            else:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.RSVP_STATUSES),
                                             Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             Attendee.approvalStatus.status.IN(constants.RSVP_STATUSES),
                                             ancestor=Attendee.get_default_event_parent_key())
        else:
            if category is not None:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.travel == category,
                                             Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.travel == category,
                                             ancestor=Attendee.get_default_event_parent_key())
            else:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.busRoute == route,
                                             ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True,
                                             ancestor=Attendee.get_default_event_parent_key())

        data = []
        for hacker in hackers:
            data.append({'nameFirst': hacker.nameFirst,
                         'nameLast': hacker.nameLast,
                         'email': hacker.email,
                         'gender': hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                         'school': hacker.school,
                         'year': hacker.year,
                         'linkedin': hacker.linkedin,
                         'github': hacker.github,
                         'shirt': hacker.shirt,
                         'food': 'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                         'projectType': hacker.projectType,
                         'resume': hacker.resume,
                         'registrationTime': hacker.registrationTime.strftime('%x %X'),
                         'isApproved': hacker.isApproved,
                         'userId': hacker.userId,
                         'travel': hacker.travel,
                         'busRoute': hacker.busRoute,
                         'approvalStatus': {'status': hacker.approvalStatus.status,
                                            'approvedTime': hacker.approvalStatus.approvedTime.strftime(
                                                '%x %X') if hacker.approvalStatus.approvedTime else None,
                                            'waitlistedTime': hacker.approvalStatus.waitlistedTime.strftime(
                                                '%x %X') if hacker.approvalStatus.waitlistedTime else None,
                                            'rsvpTime': hacker.approvalStatus.rsvpTime.strftime(
                                                '%x %X') if hacker.approvalStatus.rsvpTime else None} if hacker.approvalStatus else None,
                         'groupNumber': hacker.groupNumber})

        if not memcache.set(key, data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return data

    def set_apply_count_memcache(self):
        """Sets the 'apply_count' key in memcache"""
        q = Attendee.query(Attendee.isRegistered == True)
        cached_count = q.count()
        if not memcache.set('apply_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return cached_count

    def set_school_count_memcache(self):
        """Sets the 'school_count' key in memcache"""
        q = Attendee.query(Attendee.isRegistered == True, projection=[Attendee.school], distinct=True)
        set_of_field = set([data.school for data in q])
        cached_count = len(set_of_field)
        if not memcache.set('school_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return cached_count

    def set_approve_count_memcache(self):
        """Sets the 'approve_count' key in memcache"""
        q = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == 'Approved',
                           ancestor=Attendee.get_default_event_parent_key())
        cached_count = q.count()
        if not memcache.set('approve_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return cached_count

    def set_status_count_memcache(self, status):
        """Sets the 'status_count/<status>' key in memcache"""
        q = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status,
                           ancestor=Attendee.get_default_event_parent_key())
        cached_count = q.count()
        if not memcache.set('status_count/' + status, cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
            logging.error('Memcache set failed.')
        return cached_count

    def set_query_all_memcache(self, cls, model_type):
        key = 'query_all/' + model_type
        query = cls.search_database({})
        data = []
        for obj in query:
            data.append(obj)

        if not memcache.set(key, data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed for <%s>.' % key)

        return data


class BaseAdminTableHandler(BaseAdminHandler):
    def __init__(self, request, response):
        super(BaseAdminTableHandler, self).__init__(request, response)

    def get_db_dict(self):
        assert self.form_data is not None

        dict = {}

        for field in self.form_data['fields']:
            dict[field['db_field']] = self.request.get(field['name'])

        return dict

    def split_and_strip(self, string, split=","):
        lst = string.split(split)

        ret = []
        for item in lst:
            stripped = item.strip()
            if stripped != '':
                ret.append(stripped)

        return ret