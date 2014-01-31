import MainHandler
import cgi, urllib, logging, re
import db.models as models
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class RegisterHandler(MainHandler.Handler, blobstore_handlers.BlobstoreUploadHandler):
    """ Handler for registration page.
    This does not include the email registration we have up now."""
    def get(self):
        user = users.get_current_user()
        if user:
            db_user = models.search_database(models.Attendee, {'userId':user.user_id()}).get()
            if db_user is not None:
                return self.redirect('/profile')

            upload_url_rpc = blobstore.create_upload_url_async('/register', gs_bucket_name=constants.BUCKET)

            data = {}
            data['title'] = 'Registration'
            data['username'] = user.nickname()
            data['logoutUrl'] = users.create_logout_url('/register')
            data['email'] = user.email()
            data['genders'] = [ {'name':g} for g in constants.GENDERS ]
            data['years'] = [ {'name':y} for y in constants.STANDINGS ]
            data['shirts'] = [ {'name':s} for s in constants.SHIRTS ]
            data['foods'] = [ {'name':f} for f in constants.FOODS ]
            data['projects'] = [ {'name':p} for p in constants.PROJECTS ]

            data['resumeRequired'] = True

            data['upload_url'] = upload_url_rpc.get_result()
            self.render("register.html", data=data)

        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR')

    def post(self):
        user = users.get_current_user()
        if user:
            x = {}

            # https://developers.google.com/appengine/docs/python/users/userclass
            x['userNickname'] = user.nickname()
            x['userEmail'] = user.email()
            x['userId'] = user.user_id() #use this for identificaiton
            x['userFederatedIdentity'] = user.federated_identity()
            x['userFederatedProvider'] = user.federated_provider()

            x['nameFirst'] = self.request.get('nameFirst')
            x['nameLast'] = self.request.get('nameLast')
            x['email'] = self.request.get('email')
            x['gender'] = self.request.get('gender')
            x['school'] = self.request.get('school')
            if x['school'] == 'Other':
                x['school'] = self.request.get('schoolOther')
            x['standing'] = self.request.get('year')

            x['experience'] = self.request.get('experience')
            x['linkedin'] = self.request.get('linkedin')
            x['github'] = self.request.get('github')

            file_info = self.get_file_infos(field_name='resume')[0]

            x['resume'] = models.Resume(contentType=file_info.content_type,
                                        creationTime=file_info.creation,
                                        fileName=file_info.filename,
                                        size=file_info.size,
                                        gsObjectName=file_info.gs_object_name)

            x['shirt'] = self.request.get('shirt')
            x['food'] = self.request.get('food')
            x['foodInfo'] = self.request.get('foodInfo')

            x['teamMembers'] = self.request.get('team')
            x['projectType'] = self.request.get('projectType')
            x['userNotes'] = self.request.get('userNotes')

            x['recruiters'] = (self.request.get('recruiters') == 'True')
            x['picture'] = (self.request.get('picture') == 'True')
            x['termsOfService'] = (self.request.get('termsOfService') == 'True')
            x['approved'] = 'NA'


            valid = True

            # Check required fields filled in
            for field in constants.REQUIRED_FIELDS:
                if x[field] is None:
                    valid = False
                if isinstance(field, str) and x[field] == '':
                    valid = False

            # Check if email is valid (basic)
            if valid and not re.match(constants.EMAIL_MATCH, x['email']):
                valid = False

            # Check fields with specific values
            if valid and x['gender'] not in constants.GENDERS:
                valid = False
            if valid and x['standing'] not in constants.STANDINGS:
                valid = False
            if valid and x['shirt'] not in constants.SHIRTS:
                valid = False
            if valid and x['food'] not in constants.FOODS:
                valid = False
            if valid and x['projectType'] not in constants.PROJECTS:
                valid = False

            # Make sure required boxes checked
            if valid and not x['picture']:
                valid = False
            if valid and not x['termsOfService']:
                valid = False

            # Check resume size
            if valid and x['resume'].size <= constants.RESUME_MAX_SIZE:
                valid = False

            # if valid:
            #     models.add(models.Attendee, x)
            #     logging.info('Signup with email %s', x['email'])
            # else:
            #     # delete file
            #     pass
            # self.write(json.dumps({'valid':valid, 'message':''}))

            models.add(models.Attendee, x)
            logging.info('Signup with email %s', x['email'])
            return self.redirect('/register/complete')

        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR')


class RegisterCompleteHandler(MainHandler.Handler):
    def get(self):
        return self.render("registration_complete.html")


class SchoolCheckHandler(MainHandler.Handler):
    def get(self):
        email = urllib.unquote(self.request.get('email'))
        domain = email.split('@')[1]
        domain = domain.split('.')
        if domain[-1] != 'edu':
            return self.write('-')
        domain = domain[-2] + '.' + domain[-1]

        schools = constants.SCHOOLS
        # schools['illinois.edu'] = 'University of Illinois at Urbana-Champaign'

        if domain in schools:
            return self.write(schools[domain])
        else:
            return self.write('-')
