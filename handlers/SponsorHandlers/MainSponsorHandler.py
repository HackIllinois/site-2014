import logging
# import csv
# import cStringIO
# import random
# import pickle

from google.appengine.api import users
# from google.appengine.api import urlfetch
# from google.appengine.api import memcache

from handlers import MainHandler
# from db import constants
# from db.Attendee import Attendee
# from db.Admin import Admin
from db.Sponsor import Sponsor


class BaseSponsorHandler(MainHandler.Handler):
    """
    This is for all /sponsors pages
    Overrides the dispatch method (called before get/post/etc.)
    Sends 401 (Unauthorized) if user is not an admin
    Ref: http://webapp-improved.appspot.com/guide/handlers.html
    """

    def __init__(self, request, response):
        self.google_user = None
        self.db_user = None
        super(BaseSponsorHandler, self).__init__(request, response)

    def dispatch(self):
        self.google_user = users.get_current_user()
        if not self.google_user: return self.abort(500, detail='User not logged in')

        self.db_user = Sponsor.search_database({'userId': self.google_user.user_id()}).get()
        if not self.db_user: return self.redirect('/corporate/notregistered')

        # logging.info('%s attempted to access an admin page but was denied.', email)
        # return self.abort(401)

        logging.info('Sponsor user %s is online.', self.google_user.email())
        super(BaseSponsorHandler, self).dispatch()
