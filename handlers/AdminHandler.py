import MainHandler
import cgi, urllib, logging, re
from db.Attendee import Attendee
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class AdminHandler(MainHandler.Handler):

    def get(self):
        user = users.get_current_user()
        if user:
            name = user.nickname()
        else:
            name = 'ERROR'
        self.render('admin.html', name=name, logout=users.create_logout_url('/'))

class ApproveHandler(MainHandler.Handler):
    """ Handler for registration page.
    This does not include the email registration we have up now."""
    def get(self):
        db_all_users = models.search_database(Attendee, {'approved':'NA'})#Should Be Yes
        if db_all_users is None:
            self.response.out.write('ERROR')
        else:
            all_users = db_all_users.fetch()
        self.render('approve.html', all_users=all_users)

class ApproveResumeHandler(MainHandler.Handler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        db_user = models.search_database(Attendee, {'userId':self.request.url.split('/')[-1]}).get()
        if not db_user:
		    #Should Redirect to error page
            return self.redirect('/register')

        # https://developers.google.com/appengine/docs/python/blobstore/#Python_Using_the_Blobstore_API_with_Google_Cloud_Storage
        resource = str(urllib.unquote(db_user.resume.gsObjectName))
        blob_key = blobstore.create_gs_key(resource)
        self.send_blob(blob_key)

class AttendeeResumeHandler(MainHandler.Handler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            db_user = models.search_database(Attendee, {'userId':self.request.url.split('/')[-1]}).get()
            if not db_user:
                return self.redirect('/register')

            # https://developers.google.com/appengine/docs/python/blobstore/#Python_Using_the_Blobstore_API_with_Google_Cloud_Storage
            resource = str(urllib.unquote(db_user.resume.gsObjectName))
            blob_key = blobstore.create_gs_key(resource)
            self.send_blob(blob_key)
        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR')