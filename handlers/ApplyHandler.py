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
    # == Handler for application page. ==
    # This does not include the email registration we have up now.

    def get(self):
        user = users.get_current_user()

        if not user:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            return self.write('ERROR - Apply logged in problem')

        upload_url_rpc = blobstore.create_upload_url_async('/apply', gs_bucket_name=constants.BUCKET)

        data = {}
        data['errors'] = {} # Needed for template to render

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

            # Per-field errors
            # db_user.errors == [<field1>$$$<message1>, <field1>$$$<message2>, ...]
            if db_user.errors:
                # Turn into dictionary so template can do lookup 'data.errors.<field>'
                data['errors'] = { e.split('$$$')[0]:e.split('$$$')[1] for e in db_user.errors }

            # Previous field data
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
            if db_user.teamMembers:
                data['teamMembers'] = db_user.teamMembers

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

        data['uploadUrl'] = upload_url_rpc.get_result()
        self.render("apply.html", data=data)

    def post(self):
        user = users.get_current_user()
        if not user:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            return self.write('ERROR')

        x = {}
        errors = {} # Note: 1 error per field
        valid = True
        db_user = Attendee.search_database({'userId':user.user_id()}).get()

        # https://developers.google.com/appengine/docs/python/users/userclass
        x['userNickname'] = user.nickname()
        x['userEmail'] = user.email()
        x['userId'] = user.user_id() #use this for identification
        x['userFederatedIdentity'] = user.federated_identity()
        x['userFederatedProvider'] = user.federated_provider()

        for field in ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'experience', 'linkedin', 'github', 'teamMembers', 'shirt', 'projectType']:
           x[field] = self.request.get(field)

        file_info = self.get_file_infos(field_name='resume')
        if file_info and len(file_info) == 1:
            file_info = file_info[0]

            delete_resume = False

            if not file_info.content_type == 'application/pdf':

                # Non-pdf files
                errors['resume'] = 'Uploaded resume file is not a pdf.'
                delete_resume = True
                valid = False

            elif file_info.size > constants.RESUME_MAX_SIZE:

                # Big files
                errors['resume'] = 'Uploaded resume file is too big.'
                delete_resume = True
                valid = False

            else:

                # Old resumes
                delete_resume = db_user and db_user.resume

            # Delete resume if appropriate
            if delete_resume:
                resource = str(urllib.unquote(file_info.gs_object_name))
                blob_key = blobstore.create_gs_key(resource)
                blobstore.delete(blob_key)

            # Create new resume if appropriate
            if valid:
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
            if field is "termsOfService":
               continue

            if field not in x:
                errors[field] = constants.ERROR_MESSAGE_PREFIX + constants.READABLE_REQUIRED_FIELDS[field] + constants.ERROR_MESSAGE_SUFFIX
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
            errors['email'] = 'Invalid e-mail address.'
            valid = False

        # Check fields with specific values
        if 'gender' in x and x['gender'] not in constants.GENDERS:
            errors['gender'] = constants.ERROR_MESSAGE_PREFIX + constants.READABLE_REQUIRED_FIELDS['gender'] + constants.ERROR_MESSAGE_SUFFIX
            valid = False
        if 'year' in x and x['year'] not in constants.YEARS:
            errors['year'] = constants.ERROR_MESSAGE_PREFIX + constants.READABLE_REQUIRED_FIELDS['year'] + constants.ERROR_MESSAGE_SUFFIX
            valid = False
        if 'shirt' in x and x['shirt'] not in constants.SHIRTS:
            errors['shirt'] = constants.ERROR_MESSAGE_PREFIX + constants.READABLE_REQUIRED_FIELDS['shirt'] + constants.ERROR_MESSAGE_SUFFIX
            valid = False
        if 'food' in x and x['food'] != '':
            temp = x['food'].split(',')
            if 'Other' in temp and ('foodInfo' not in x or ('foodInfo' in x and x['foodInfo'] == '')):
                errors['food'] += constants.ERROR_MESSAGE_PREFIX + constants.READABLE_FIELDS['food'] + constants.ERROR_MESSAGE_SUFFIX
                valid = False

            for f in x['food'].split(','):
                if f not in constants.FOODS:
                    errors['food'] = constants.ERROR_MESSAGE_PREFIX + constants.READABLE_FIELDS['food'] + constants.ERROR_MESSAGE_SUFFIX
                    valid = False
                    break # This is why we need the for loop below


        if 'projectType' in x and x['projectType'] not in constants.PROJECTS:
            errors['projectType'] = constants.ERROR_MESSAGE_PREFIX + constants.READABLE_FIELDS['projectType'] + constants.ERROR_MESSAGE_SUFFIX
            valid = False

        # Make sure required boxes checked
        if not ('termsOfService' in x) or not x['termsOfService']:
            errors['termsOfService'] = 'Please read and agree to the rules and code of conduct.'
            valid = False

        # Create list of error messages
        x['errors'] = [ k + '$$$' + errors[k] for k in errors ]

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
        school_list = sorted(list((set(schools))))
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
