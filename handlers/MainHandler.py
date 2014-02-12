import os
import jinja2
import webapp2
import logging
from google.appengine.api import users
from db import constants

template_dir = os.path.join(os.path.dirname(__file__), os.path.join(os.pardir, 'templates'))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

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
    Sends 403 (forbidden) if user is not an admin
    Ref: http://webapp-improved.appspot.com/guide/handlers.html
    """
    def dispatch(self):
        is_admin = False

        user = users.get_current_user()
        if not user:
            return self.abort(404)

        email = user.email()
        domain = email.split('@')[1] if len(email.split('@')) == 2 else None # Sanity check

        if domain == 'hackillinois.org' or email in constants.ADMIN_EMAILS:
            is_admin = True

        if is_admin:
            # Parent class will call the method to be dispatched
            # -- get() or post() or etc.
            logging.info('Admin user %s is online.', email)
            super(BaseAdminHandler, self).dispatch()
        else:
            logging.info('%s attempted to access an admin page but was denied.', email)
            return self.render( "simple_message.html",
                                header="ACCESS DENIED",
                                message="You (%s) are not an admin or are not logged in as such.<br>Please log in with a valid @hackillinois.org email address.<br><a class='logout-link' href='%s'>Logout</a>" % (user.nickname(), users.create_logout_url('/admin')),
                                showSocial=False )