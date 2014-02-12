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

class SummaryHandler(MainHandler.Handler):
    def get(self):
        user = users.get_current_user()
        if not user:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            return self.write('ERROR - User not logged in.')

        email = user.email()
        email = email.split('@')
        if len(email) != 2 or (len(email) == 2 and email[1] != 'hackillinois.org'):
            return self.render( "simple_message.html",
                                header="ACCESS DENIED",
                                message="You (%s) are not an admin or are not logged in as such.<br>Please log in with a valid @hackillinois.org email address.<br><a class='logout-link' href='%s'>Logout</a>" % (user.nickname(), users.create_logout_url('/admin')),
                                showSocial=False )


        hackers = Attendee.search_database({})
        data = {}
        data['hackers'] = []
        for hacker in hackers:
            data['hackers'].append({ 'nameFirst':hacker.nameFirst,
                                     'nameLast':hacker.nameLast,
                                     'email':hacker.email,
                                     'gender':hacker.gender,
                                     'school':hacker.school,
                                     'year':hacker.year,
                                     'linkedin':hacker.linkedin,
                                     'github':hacker.github,
                                     'shirt':hacker.shirt,
                                     'food':hacker.food,
                                     'projectType':hacker.projectType,
                                     'registrationTime':str(hacker.registrationTime),
                                     'approved':hacker.approved })

        self.render("summary.html", data=data)