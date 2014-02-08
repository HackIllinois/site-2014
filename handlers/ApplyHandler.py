import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db.Resume import Resume
from db import constants
from google.appengine.api import users, memcache
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import json

# from datetime import datetime
# import json
# from google.appengine.api import mail


# def SendApplyEmail(subject, body):
#     body_str = json.dumps(body)
#     logging.info("Sent email '%s'",  subject)
#     mail.send_mail(sender="alex.burck@hackillinois.org",
#                    to="apply-watchlist@hackillinois.org",
#                    subject=subject,
#                    body=body_str)


class ApplyHandler(MainHandler.Handler, blobstore_handlers.BlobstoreUploadHandler):
    """ Handler for application page.
    This does not include the email registration we have up now."""

    def get(self):
        user = users.get_current_user()

        if not user:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            return self.write('ERROR - Apply logged in problem')

        data = {}
        data['username'] = user.nickname()
        data['logoutUrl'] = users.create_logout_url('/apply')
        data['email'] = user.email()
        data['genders'] = [ {'name':g, 'checked':False} for g in constants.GENDERS ]
        data['years'] = [ {'name':y, 'checked':False} for y in constants.YEARS ]
        data['shirts'] = [ {'name':s, 'checked':False} for s in constants.SHIRTS ]
        data['foods'] = [ {'name':f, 'checked':False} for f in constants.FOODS ]
        data['projects'] = [ {'name':p, 'selected':False} for p in constants.PROJECTS ]

        data['title'] = constants.APPLY_TITLE
        data['resumeRequired'] = False
        data['hasResume'] = False
        data['applyError'] = False
        data['uploadUrl'] = '/apply'

        # Check if user is in our database
        db_user = Attendee.search_database({'userId': user.user_id()}).get()
        if db_user is not None:
            if db_user.isRegistered:
                data['isUpdatingApplication'] = True
                data['title'] = constants.PROFILE_TITLE
                data['resumeRequired'] = False

            if db_user.applyError:
                data['applyError'] = True

            if db_user.nameFirst:
                data['nameFirst'] = db_user.nameFirst
            if db_user.nameLast:
                data['nameLast'] = db_user.nameLast
            if db_user.email:
                data['email'] = db_user.email
            if db_user.school:
                data['school'] = db_user.school
            if db_user.experience:
                data['experience'] = db_user.experience
            if db_user.linkedin:
                data['linkedin'] = db_user.linkedin
            if db_user.github:
                data['github'] = db_user.github
            if db_user.foodInfo:
                data['foodInfo'] = db_user.foodInfo
            if db_user.termsOfService:
                data['termsOfService'] = db_user.termsOfService

            if db_user.gender:
                for i in data['genders']:
                    if i['name'] == db_user.gender:
                        i['checked'] = True
                        break

            if db_user.year:
                for i in data['years']:
                    if i['name'] == db_user.year:
                        i['checked'] = True
                        break

            if db_user.shirt:
                for i in data['shirts']:
                    if i['name'] == db_user.shirt:
                        i['checked'] = True
                        break

            if db_user.food:
                for i in data['foods']:
                    if i['name'] in db_user.food:
                        i['checked'] = True

            if db_user.projectType:
                for i in data['projects']:
                    if i['name'] == db_user.projectType:
                        i['selected'] = True
                        break

            if db_user.resume:
                data['hasResume'] = True
                data['resumeRequired'] = False

            if db_user.errorMessages and db_user.errorMessages != '':
                data['messages'] = db_user.errorMessages.split('$$$')

        self.render("apply.html", data=data)

    def post(self):
        user = users.get_current_user()
        if not user:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            return self.write('ERROR')

        x = {}
        valid = True
        errorMessages = []
        db_user = Attendee.search_database({'userId':user.user_id()}).get()

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
        x['year'] = self.request.get('year')
        x['experience'] = self.request.get('experience')
        x['linkedin'] = self.request.get('linkedin')
        x['github'] = self.request.get('github')

        x['shirt'] = self.request.get('shirt')
        x['projectType'] = self.request.get('projectType')
        # x['teamMembers'] = self.request.get('team')

        file_info = self.get_file_infos(field_name='resume')
        if file_info and len(file_info) == 1:
            file_info = file_info[0]
            if not file_info.content_type == 'application/pdf':
                errorMessages.append('Uploaded resume file is not a pdf.')

                # Delete non pdf file
                resource = str(urllib.unquote(file_info.gs_object_name))
                blob_key = blobstore.create_gs_key(resource)
                blobstore.delete(blob_key)

                valid = False
            elif file_info.size > constants.RESUME_MAX_SIZE:
                errorMessages.append('Uploaded resume file is too big.')

                # Delete big file
                resource = str(urllib.unquote(file_info.gs_object_name))
                blob_key = blobstore.create_gs_key(resource)
                blobstore.delete(blob_key)

                valid = False
            else:
                if db_user and db_user.resume:
                    # Delete old resume
                    resource = str(urllib.unquote(db_user.resume.gsObjectName))
                    blob_key = blobstore.create_gs_key(resource)
                    blobstore.delete(blob_key)

                x['resume'] = Resume(contentType=file_info.content_type,
                                     creationTime=file_info.creation,
                                     fileName=file_info.filename,
                                     size=file_info.size,
                                     gsObjectName=file_info.gs_object_name)

        foods = self.request.get_all('food')
        x['food'] = ','.join(foods)
        x['foodInfo'] = self.request.get('foodInfo')

        x['termsOfService'] = (self.request.get('termsOfService') == 'True')
        if not x['termsOfService']:
            if db_user is not None:
                x['termsOfService'] = db_user.termsOfService

        # Remove any empty fields
        for field in constants.ALL_FIELDS:
            if field in x and not x[field]:
                # This checks for None and '' and u''
                del x[field]

        # Check required fields filled in
        for field in constants.REQUIRED_FIELDS:
            if field not in x:
                errorMessages.append(constants.ERROR_MESSAGE_PREFIX + constants.FIELD_DISPLAY_NAMES[field] + constants.ERROR_MESSAGE_SUFFIX)
                valid = False

        # Check if hame has a number in it
        # if 'nameFirst' in x and any(char.isdigit() for char in x['nameFirst']):
        #     errorMessages.append('Your first name cannot have an Arabic numeral in it.')
        #     valid = False
        # if 'nameLast' in x and any(char.isdigit() for char in x['nameLast']):
        #     errorMessages.append('Your last name cannot have an Arabic numeral in it.')
        #     valid = False

        # Check if email is valid (basic)
        if 'email' in x and not re.match(constants.EMAIL_MATCH, x['email']):
            errorMessages.append('Uploaded file is too big.')
            valid = False

        # Check fields with specific values
        if 'gender' in x and x['gender'] not in constants.GENDERS:
            errorMessages.append(constants.ERROR_MESSAGE_PREFIX + constants.FIELD_DISPLAY_NAMES['gender'] + constants.ERROR_MESSAGE_SUFFIX)
            valid = False
        if 'year' in x and x['year'] not in constants.YEARS:
            errorMessages.append(constants.ERROR_MESSAGE_PREFIX + constants.FIELD_DISPLAY_NAMES['year'] + constants.ERROR_MESSAGE_SUFFIX)
            valid = False
        if 'shirt' in x and x['shirt'] not in constants.SHIRTS:
            errorMessages.append(constants.ERROR_MESSAGE_PREFIX + constants.FIELD_DISPLAY_NAMES['shirt'] + constants.ERROR_MESSAGE_SUFFIX)
            valid = False
        if 'food' in x and x['food'] != '':
            for f in x['food'].split(','):
                if f not in constants.FOODS:
                    errorMessages.append(constants.ERROR_MESSAGE_PREFIX + constants.FIELD_DISPLAY_NAMES['food'] + constants.ERROR_MESSAGE_SUFFIX)
                    valid = False
                    break
        if 'projectType' in x and x['projectType'] not in constants.PROJECTS:
            errorMessages.append(constants.ERROR_MESSAGE_PREFIX + constants.FIELD_DISPLAY_NAMES['projectType'] + constants.ERROR_MESSAGE_SUFFIX)
            valid = False

        # Make sure required boxes checked
        if 'termsOfService' not in x or ('termsOfService' in x and not x['termsOfService']):
            errorMessages.append('Please read and agree to the rules and code of conduct.')
            valid = False

        x['errorMessages'] = '$$$'.join(errorMessages)

        if valid:
            x['isRegistered'] = True
            x['applyError'] = False
            redir = '/apply/complete'

            memcache.incr('apply_count')
        else:
            x['applyError'] = True
            redir = '/apply'

        if db_user is not None:
            if valid:
                if db_user.isRegistered:
                    redir = '/apply/updated'
                    logging.info('Updated profile of %s', x['email'])
                    logging.info(str(x))
                    # SendApplyEmail('Updated profile of ' + x['email'], x)
                else:
                    redir = '/apply/complete'
                    logging.info('Signup with email %s', x['email'])
                    logging.info(str(x))
                    # SendApplyEmail('Signup with email ' + x['email'], x)
            success = Attendee.update_search(x, {'userId':x['userId']})
        else:
            if valid:
                logging.info('Signup with email %s', x['email'])
                logging.info(str(x))
                # SendApplyEmail('Signup with email ' + x['email'], x)
            else:
                logging.info('User with email %s submitted an invalid form', x['email'])
            success = Attendee.add(x)

        return self.redirect(redir)


class ApplyCompleteHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header=constants.APPLY_COMPLETE_HEADER,
                            message=constants.APPLY_COMPLETE_MESSAGE,
                            showSocial=True )


class UpdateCompleteHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header=constants.UPDATE_COMPLETE_HEADER,
                            message=constants.UPDATE_COMPLETE_MESSAGE,
                            showSocial=True )


class SchoolCheckHandler(MainHandler.Handler):
    def get(self):
        email = urllib.unquote(self.request.get('email'))
        if(len(email.split('@')) == 1):
            return self.write('-')
        domain = email.split('@')[1]
        domain = domain.split('.')
        if domain[-1] != 'edu':
            if len(domain) > 1:
                return self.write('--')
            else:
                return self.write('-')
        domain = domain[-2] + '.' + domain[-1]

        schools = constants.SCHOOLS

        if domain in schools:
            return self.write(schools[domain])
        else:
            return self.write('--')


class SchoolListHandler(MainHandler.Handler):
    def get(self):
        schools = constants.SCHOOLS
        school_list = list(set([schools[i] for i in schools]))
        out_list = [{'name':school} for school in school_list]
        self.write(json.dumps({'schools': out_list}))


class MyResumeHandler(MainHandler.Handler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            return self.write('ERROR - Unexpected resume login')

        db_user = Attendee.search_database({'userId':user.user_id()}).get()
        if not db_user:
            return self.redirect('/apply')

        logging.info('Retrieving resume for %s', db_user.email)

        # https://developers.google.com/appengine/docs/python/blobstore/#Python_Using_the_Blobstore_API_with_Google_Cloud_Storage
        resource = str(urllib.unquote(db_user.resume.gsObjectName))
        blob_key = blobstore.create_gs_key(resource)
        return self.send_blob(blob_key)

class UploadURLHandler(MainHandler.Handler):
    def get(self):
        upload_url = blobstore.create_upload_url('/apply', gs_bucket_name=constants.BUCKET)
        self.write(json.dumps({'upload_url': upload_url}))
