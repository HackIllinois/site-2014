import os
import jinja2
import webapp2
import logging
from google.appengine.api import users
from db import constants
from google.appengine.ext import ereporter
from db.Admin import Admin

template_dir = os.path.join(os.path.dirname(__file__), os.path.join(os.pardir, 'templates'))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# https://developers.google.com/appengine/articles/python/recording_exceptions_with_ereporter
ereporter.register_logger()


class Handler(webapp2.RequestHandler):
    """ Someone should fill in what this is """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(self.render_str(template,**kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        page = t.render(params)

        return page


class BaseAdminHandler(Handler):
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


class BaseMobileHandler(Handler):

    def dispatch(self):
        if 'AuthName' in self.request.headers:
            userId = self.request.headers['AuthName']
        else:
            userId = None

        if userId == 'test':
            super(BaseMobileHandler, self).dispatch()
        elif userId:
            db_user = Attendee.search_database({'userId':userId}).get()
            super(BaseMobileHandler, self).dispath()
        else:
            return self.write('Did not pass userId')
