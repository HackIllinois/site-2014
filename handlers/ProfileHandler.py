import MainHandler
import cgi, urllib, logging, re
import db.models as models
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class ProfileHandler(MainHandler.Handler, blobstore_handlers.BlobstoreUploadHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            db_user = models.search_database(models.Attendee, {'userId':user.user_id()}).get()
            if db_user is None:
                return self.redirect('/apply')

            upload_url_rpc = blobstore.create_upload_url_async('/profile', gs_bucket_name=constants.BUCKET)

            data = {}
            data['title'] = 'Profile'
            data['username'] = user.nickname()
            data['logoutUrl'] = users.create_logout_url('/')
            data['nameFirst'] = db_user.nameFirst
            data['nameLast'] = db_user.nameLast
            data['email'] = db_user.email
            data['genders'] = [ {'name':g, 'checked':False} for g in constants.GENDERS ]
            for i in data['genders']:
                if i['name'] == db_user.gender:
                    i['checked'] = True
                    break
            data['school'] = db_user.school
            data['years'] = [ {'name':y, 'checked':False} for y in constants.STANDINGS ]
            for i in data['years']:
                if i['name'] == db_user.standing:
                    i['checked'] = True
                    break
            data['experience'] = db_user.experience
            data['linkedin'] = db_user.linkedin
            data['github'] = db_user.github
            data['shirts'] = [ {'name':s, 'checked':False} for s in constants.SHIRTS ]
            for i in data['shirts']:
                if i['name'] == db_user.shirt:
                    i['checked'] = True
                    break
            data['foods'] = [ {'name':f, 'checked':False} for f in constants.FOODS ]
            for i in data['foods']:
                if i['name'] == db_user.food:
                    i['checked'] = True
                    break
            data['foodInfo'] = db_user.foodInfo
            data['team'] = db_user.teamMembers
            data['projects'] = [ {'name':p, 'selected':False} for p in constants.PROJECTS ]
            for i in data['projects']:
                if i['name'] == db_user.projectType:
                    i['selected'] = True
                    break
            data['userNotes'] = db_user.userNotes
            data['picture'] = db_user.picture
            data['termsOfService'] = db_user.termsOfService

            data['resumeRequired'] = False

            data['upload_url'] = upload_url_rpc.get_result()
            self.render("apply.html", data=data)

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

            file_info = self.get_file_infos(field_name='resume')
            valid = True
            if file_info:
                if len(file_info) == 1 and file_info[0].file_name.endswith(".pdf"):
                    file_info = file_info[0]
                    x['resume'] = models.Resume(contentType=file_info.content_type,
                                            creationTime=file_info.creation,
                                            fileName=file_info.filename,
                                            size=file_info.size,
                                            gsObjectName=file_info.gs_object_name)
                else:
                    valid = False # A resume was uploaded, but it wasn't what we want

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
            if valid and x['resume'] and x['resume'].size <= constants.RESUME_MAX_SIZE and x['resume']:
                valid = False

            # Remove any keys that are not updated
            for key in list(x):
                if x[key] is None or x[key] == '':
                    del x[key]

            # if valid:
            #     models.add(models.Attendee, x)
            #     logging.info('Signup with email %s', x['email'])
            # else:
            #     # delete file
            #     pass
            # self.write(json.dumps({'valid':valid, 'message':''}))

            models.update_search(models.Attendee, x, {'userId':user.user_id()})
            logging.info('Updated profile of %s', x['email'])
            return self.redirect('/profile/updated')

        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR - Unexpected profile login')


class UpdateCompleteHandler(MainHandler.Handler):
    def get(self):
        return self.render("simple_message.html", message="Update Successful!")


class MyResumeHandler(MainHandler.Handler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            db_user = models.search_database(models.Attendee, {'userId':user.user_id()}).get()
            if not db_user:
                return self.redirect('/apply')

            # https://developers.google.com/appengine/docs/python/blobstore/#Python_Using_the_Blobstore_API_with_Google_Cloud_Storage
            resource = str(urllib.unquote(db_user.resume.gsObjectName))
            blob_key = blobstore.create_gs_key(resource)
            self.send_blob(blob_key)
        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR - Unexpected resume login')
