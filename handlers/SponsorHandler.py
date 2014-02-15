import MainHandler
import cgi, urllib, logging, re, datetime
from db.Attendee import Attendee
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class SponsorHandler(MainHandler.BaseAdminHandler):
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
                                     'food':'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                                     'projectType':hacker.projectType,
                                     'registrationTime':hacker.registrationTime.strftime('%x %X'),
                                     'resume':resume_link,
                                     'approved':hacker.approved,
                                     'userId':hacker.userId})

        self.render("approve.html", data=data)
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

class AdminStatsHandler(MainHandler.BaseAdminHandler):
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
                                     'food':'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                                     'projectType':hacker.projectType,
                                     'registrationTime':hacker.registrationTime.strftime('%x %X'),
                                     'resume':resume_link,
                                     'approved':hacker.approved,
                                     'userId':hacker.userId})

        self.render("approve.html", data=data)
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