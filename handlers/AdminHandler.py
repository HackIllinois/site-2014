import MainHandler
import cgi, urllib, logging, re, datetime
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


class AdminResumeHandler(MainHandler.BaseAdminHandler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        userId = str(urllib.unquote(self.request.get('userId')))
        db_user = Attendee.search_database({'userId':userId}).get()
        if not db_user:
            return self.render( "simple_message.html",
                                header="Not Available",
                                message="User ID is not valid.",
                                showSocial=False )

        if not db_user.resume:
            return self.render( "simple_message.html",
                                header="Not Available",
                                message="User has not uploaded a resume.",
                                showSocial=False )

        # https://developers.google.com/appengine/docs/python/blobstore/#Python_Using_the_Blobstore_API_with_Google_Cloud_Storage
        resource = str(urllib.unquote(db_user.resume.gsObjectName))
        blob_key = blobstore.create_gs_key(resource)
        return self.send_blob(blob_key)


class SummaryHandler(MainHandler.BaseAdminHandler):
    def get(self):
        hackers = Attendee.search_database({'isRegistered':True})
        data = {}
        data['hackers'] = []
        for hacker in hackers:
            resume_link = None
            if hacker.resume:
                name = hacker.resume.fileName
                name = name if len(name)<=10 else name[0:7]+'...'
                resume_link = "<a href='/admin/resume?userId=%s'>%s</a>" % (hacker.userId, name)
                pass
            else:
                resume_link = ''

            data['hackers'].append({ 'nameFirst':hacker.nameFirst,
                                     'nameLast':hacker.nameLast,
                                     'email':hacker.email,
                                     'gender':hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                                     'school':hacker.school,
                                     'year':hacker.year,
                                     'linkedin':hacker.linkedin,
                                     'github':hacker.github,
                                     'shirt':hacker.shirt,
                                     'food':'' if not hacker.food else ', '.join(hacker.food.split(',')),
                                     'projectType':hacker.projectType,
                                     'registrationTime':hacker.registrationTime.strftime('%x %X'),
                                     'resume':resume_link,
                                     'approved':hacker.approved,
                                     'userId':hacker.userId})

        self.render("summary.html", data=data)
    def post(self):
        userid = str(self.request.get('id'))
        user = Attendee.search_database({'userId':userid}).get() #works now
        if not user:
           # TODO: redirect to error handler
            return self.write('ERROR')
        x = {}
        x['approved'] = 'True'
        success = Attendee.update_search(x, {'userId':userid})

        #return self.redirect("/admin") #unnessicary