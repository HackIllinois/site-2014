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

    def get_admin_user():
        """Returns the database Admin model for the current logged-in user"""
        user = users.get_current_user()
        if not user: return None
        admin_user = Admin.search_database({'email': user.email()}).get()
        if not admin_user: return None
        return admin_user

    def set_hackers_memcache():
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

    def get_hackers_memecache():
        """Gets the 'hackers' key from the memcache and updates the memcache if the key is not in the memcache"""
        data = memcache.get('hackers')
        if not data:
            data = set_hackers_memcache()

        stats = memcache.get_stats()
        logging.info('Hackers:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        return data

    def get_hackers_csv_memcache(base_url):
        """Gets the 'hackers_csv' key from the memcache and updates the memcache if the key is not in the memcache"""
        csv_string = memcache.get('hackers_csv')
        if not csv_string:
            hackers = get_hackers_memecache()
            output = cStringIO.StringIO()
            writer = csv.writer(output)

            fields = ['nameFirst','nameLast','email',
                      'gender','school','year','linkedin',
                      'github','shirt','food','projectType',
                      'registrationTime','isApproved','userId']

            writer.writerow(constants.CSV_HEADINGS)
            for h in hackers:
                row = []
                for f in fields:
                    if f in h and h[f] is not None:
                        row.append(h[f])
                    else:
                        row.append('')
                if 'resume' in h and h['resume'] is not None:
                    row.append(base_url + '/admin/resume?userId='+h['userId'])
                else:
                    row.append('')

                writer.writerow(row)

            csv_string = output.getvalue()
            output.close()

            if not memcache.add('hackers_csv', csv_string, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Hackers CSV:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        return csv_string