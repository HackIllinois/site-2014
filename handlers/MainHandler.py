import os
import jinja2
import webapp2
from google.appengine.ext import ereporter
from db.Attendee import Attendee

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


class BaseMobileHandler(Handler):

    def dispatch(self):
        super(BaseMobileHandler, self).dispatch()
