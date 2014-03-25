import urllib
import logging
import re
import json

import MainHandler

from db.Attendee import Attendee
from db.Resume import Resume
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class RsvpHandler(MainHandler.Handler):
    def get(self):
        user = users.get_current_user()
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')
		
        db_user = Attendee.search_database({'userId': user.user_id()}).get()
		
        # Login Page
        if db_user is None:
		    return self.redirect('/apply/closed')

        if db_user is not None and (db_user.isRegistered == False):
            return self.redirect('/apply/closed')
			
		#Not yet approved page
        if db_user is not None and (db_user.isApproved == False):
            return self.redirect('/apply/closed')

        data = {}
        data['title'] = constants.RSVP_TITLE
        data['errors'] = {} # Needed for template to render
		
        data['username'] = db_user.userNickname
        data['email'] = db_user.email
        data['uploadUrl'] = blobstore.create_upload_url('/apply/update', gs_bucket_name=constants.BUCKET)
        data['logoutUrl'] = users.create_logout_url('/apply')
		
        self.render("rsvp.html", data=data)

    def post(self):
        pass