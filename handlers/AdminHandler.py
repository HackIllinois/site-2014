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


class AdminApproveHandler(MainHandler.BaseAdminHandler):
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

class AdminStatsHandler(MainHandler.BaseAdminHandler):
    def get(self):
        hackers = Attendee.search_database({'isRegistered':True})
  
        data = {}
        data['total'] = {}
        data['total']['male'] = 0
        data['total']['female'] = 0
        data['total']['other'] = 0
        data['total']['freshman'] = 0
        data['total']['sophomore'] = 0
        data['total']['junior'] = 0
        data['total']['senior'] = 0
        data['total']['grad'] = 0
        data['total']['hs'] = 0
        data['total']['xs'] = 0
        data['total']['s'] = 0
        data['total']['m'] = 0
        data['total']['l'] = 0
        data['total']['xl'] = 0
        data['total']['xxl'] = 0
        data['total']['vegetarian'] = 0
        data['total']['vegan'] = 0				
        data['total']['gluten'] = 0				
        data['total']['lactose'] = 0				
        data['total']['otherfood'] = 0
        data['total']['software'] = 0
        data['total']['hardware'] = 0
        data['total']['unsure'] = 0
		
        for hacker in hackers:
            if hacker.school not in data:
                data[hacker.school] = {}
                data[hacker.school]['name'] = hacker.school
                data[hacker.school]['male'] = 0
                data[hacker.school]['female'] = 0
                data[hacker.school]['other'] = 0
                data[hacker.school]['freshman'] = 0
                data[hacker.school]['sophomore'] = 0
                data[hacker.school]['junior'] = 0
                data[hacker.school]['senior'] = 0
                data[hacker.school]['grad'] = 0
                data[hacker.school]['hs'] = 0
                data[hacker.school]['xs'] = 0
                data[hacker.school]['s'] = 0
                data[hacker.school]['m'] = 0
                data[hacker.school]['l'] = 0
                data[hacker.school]['xl'] = 0
                data[hacker.school]['xxl'] = 0
                data[hacker.school]['vegetarian'] = 0
                data[hacker.school]['vegan'] = 0				
                data[hacker.school]['gluten'] = 0				
                data[hacker.school]['lactose'] = 0				
                data[hacker.school]['otherfood'] = 0
                data[hacker.school]['software'] = 0
                data[hacker.school]['hardware'] = 0
                data[hacker.school]['unsure'] = 0
            if hacker.gender.lower() == 'i choose not to specify':
                data[hacker.school]['other'] = data[hacker.school]['other'] + 1
                data['total']['other'] = data['total']['other'] + 1
            else:
                data[hacker.school][hacker.gender.lower()] = data[hacker.school][hacker.gender.lower()] + 1
                data['total'][hacker.gender.lower()] = data['total'][hacker.gender.lower()] + 1
            data[hacker.school][hacker.year.lower()] = data[hacker.school][hacker.year.lower()] + 1
            data['total'][hacker.year.lower()] = data['total'][hacker.year.lower()] + 1
            data[hacker.school][hacker.shirt.lower()] = data[hacker.school][hacker.shirt.lower()] + 1
            data['total'][hacker.shirt.lower()] = data['total'][hacker.shirt.lower()] + 1
            if hacker.food:
                for food in hacker.food.lower().split(','):
                    if food == 'other':
                        data[hacker.school]['otherfood'] = data[hacker.school]['otherfood'] + 1
                        data['total']['otherfood'] = data['total']['otherfood'] + 1
                    else:
                        data[hacker.school][food.split()[0]] = data[hacker.school][food.split()[0]] + 1
                        data['total'][food.split()[0]] = data['total'][food.split()[0]] + 1
            data[hacker.school][hacker.projectType.lower().split()[0]] = data[hacker.school][hacker.projectType.lower().split()[0]] + 1
            data['total'][hacker.projectType.lower().split()[0]] = data['total'][hacker.projectType.lower().split()[0]] + 1
        schools = {}
        schools['schools'] = []
        schools['total'] = []
        sort = []
        for x in data:
            sort.append(str(x))
        sort = sorted(sort, key=str.lower)
        for x in sort:
            if x != 'total':
                schools['schools'].append({'name':data[x]['name'],
                                'total':data[x]['male'] + data[x]['female'] + data[x]['other'],
                                'male':data[x]['male'],
                                'female':data[x]['female'],
                                'other':data[x]['other'],
                                'freshman':data[x]['freshman'],
                                'sophomore':data[x]['sophomore'],
                                'junior':data[x]['junior'],
                                'senior':data[x]['senior'],
                                'grad':data[x]['grad'],
                                'hs':data[x]['hs'],
                                'xs':data[x]['xs'],
                                's':data[x]['s'],
                                'm':data[x]['m'],
                                'l':data[x]['l'],
                                'xl':data[x]['xl'],
                                'xxl':data[x]['xxl'],
                                'vegetarian':data[x]['vegetarian'],
                                'vegan':data[x]['vegan'],            
                                'gluten':data[x]['gluten'],                
                                'lactose':data[x]['lactose'],                
                                'otherfood':data[x]['otherfood'],
                                'software':data[x]['software'],
                                'hardware':data[x]['hardware'],
                                'unsure':data[x]['unsure'] })
        schools['total'].append({'total':data['total']['male'] + data['total']['female'] + data['total']['other'],
                        'male':data['total']['male'],
                        'female':data['total']['female'],
                        'other':data['total']['other'],
                        'freshman':data['total']['freshman'],
                        'sophomore':data['total']['sophomore'],
                        'junior':data['total']['junior'],
                        'senior':data['total']['senior'],
                        'grad':data['total']['grad'],
                        'hs':data['total']['hs'],
                        'xs':data['total']['xs'],
                        's':data['total']['s'],
                        'm':data['total']['m'],
                        'l':data['total']['l'],
                        'xl':data['total']['xl'],
                        'xxl':data['total']['xxl'],
                        'vegetarian':data['total']['vegetarian'],
                        'vegan':data['total']['vegan'],            
                        'gluten':data['total']['gluten'],                
                        'lactose':data['total']['lactose'],                
                        'otherfood':data['total']['otherfood'],
                        'software':data['total']['software'],                                    
                        'hardware':data['total']['hardware'],
                        'unsure':data['total']['unsure'] })
        self.render("stats.html", schools=schools)