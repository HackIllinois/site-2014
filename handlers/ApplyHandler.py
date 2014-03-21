
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


class ApplyHandler(MainHandler.Handler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')

        data = {}
        data['errors'] = {} # Needed for template to render

        data['username'] = user.nickname()
        data['logoutUrl'] = users.create_logout_url('/apply')
        data['email'] = user.email()

        lists = {
            'genders':constants.GENDERS, 'years':constants.YEARS, 'shirts':constants.SHIRTS,
            'foods':constants.FOODS, 'projects':constants.PROJECTS, 'travelArrangements':constants.TRAVEL_ARRANGEMENTS
        }
        for l, options in lists.iteritems(): data[l] = [ {'name':n, 'checked':False} for n in options ]

        data['busRoutes'] = [ {'name':n, 'selected':False} for n in constants.BUS_ROUTES ]

        data['title'] = constants.APPLY_TITLE
        data['hasResume'] = False

        # Check if user is in our database
        db_user = Attendee.search_database({'userId': user.user_id()}).get()
        if db_user:
            if db_user.isRegistered:
                data['isUpdatingApplication'] = True
                data['title'] = constants.PROFILE_TITLE

            # Per-field errors
            # db_user.errors == [<field1>$$$<message1>, <field1>$$$<message2>, ...]
            if db_user.errors:
                # Turn into dictionary so template can do lookup 'data.errors.<field>'
                data['errors'] = { e.split('$$$')[0]:e.split('$$$')[1] for e in db_user.errors }

            text_fields = [
                'nameFirst', 'nameLast', 'email', 'school',
                'experience', 'linkedin', 'github', 'foodInfo',
                'teamMembers'
            ]
            for field in text_fields:
                value = getattr(db_user, field) # Gets db_user.field using a string
                if value: data[field] = value

            choose_one_fields = {
                'gender':('genders','checked'), 'year':('years','checked'),
                'shirt':('shirts','checked'), 'projectType':('projects','selected'),
                'travel':('travelArrangements','checked'), 'busRoute':('busRoutes','selected')
            }
            for field, conn in choose_one_fields.iteritems():
                value = getattr(db_user, field)
                if value:
                    for i in data[conn[0]]:
                        if i['name'] == value:
                            i[conn[1]] = True
                            break

            # Multi-choice check box
            food = db_user.food
            if food:
                for i in data['foods']:
                    if i['name'] in food: i['checked'] = True

            if db_user.resume and db_user.resume.fileName:
                data['hasResume'] = True

            if db_user.termsOfService:
                data['termsOfService'] = True

        data['uploadUrl'] = blobstore.create_upload_url('/apply', gs_bucket_name=constants.BUCKET)
        self.render("apply.html", data=data)

    def post(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')

        # Initialization
        x = {} # dictionary that will be used to create a new Attendee or update one
        errors = {} # Note: 1 error per field
        valid = True
        db_user = Attendee.search_database({'userId':user.user_id()}).get()

        # Save user information
        # https://developers.google.com/appengine/docs/python/users/userclass
        x['userNickname'] = user.nickname()
        x['userEmail'] = user.email()
        x['userId'] = user.user_id() #use this for identification
        x['userFederatedIdentity'] = user.federated_identity()
        x['userFederatedProvider'] = user.federated_provider()

        x['googleUser'] = user


        # Get data from form
        fields = [
            'nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'experience',
            'linkedin', 'github', 'teamMembers', 'shirt', 'projectType', 'travel', 'busRoute'
        ]
        for field in fields:
           x[field] = self.request.get(field)

        foods = self.request.get_all('food')
        x['food'] = ','.join(foods)
        x['foodInfo'] = self.request.get('foodInfo')

        x['termsOfService'] = (self.request.get('termsOfService') == 'True')
        if not x['termsOfService'] and db_user:
            x['termsOfService'] = db_user.termsOfService


        # Get resume data
        file_info = self.get_file_infos(field_name='resume')
        if file_info and len(file_info) == 1:
            file_info = file_info[0]
            delete_file = False

            # Non-pdf files
            # if not file_info.content_type == 'application/pdf':
            if not file_info.filename[-4:] == '.pdf':
                errors['resume'] = 'Uploaded resume file is not a pdf.'
                delete_file = True
                valid = False

            # Big files
            elif file_info.size > constants.RESUME_MAX_SIZE:
                errors['resume'] = 'Uploaded resume file is too big.'
                delete_file = True
                valid = False

            # Delete uploaded file if appropriate
            if delete_file:
                resource = str(urllib.unquote(file_info.gs_object_name))
                blob_key = blobstore.create_gs_key(resource)
                blobstore.delete(blob_key)

            # Uploaded file is valid, delete old resume if there is one and save new resume
            else:
                # Delete old resume
                if db_user and db_user.resume and db_user.resume.gsObjectName:
                    resource = str(urllib.unquote(db_user.resume.gsObjectName))
                    blob_key = blobstore.create_gs_key(resource)
                    blobstore.delete(blob_key)

                # Save new resume
                x['resume'] = Resume(contentType=file_info.content_type,
                                     creationTime=file_info.creation,
                                     fileName=file_info.filename,
                                     size=file_info.size,
                                     gsObjectName=file_info.gs_object_name)


        # Remove any empty fields from x
        for field in constants.ALL_FIELDS:
            # This checks for None and '' and u''
            if field in x and not x[field]:
                del x[field]


        # ---------- BEGIN VALIDATION ----------

        # Check required fields filled in
        for field in constants.REQUIRED_FIELDS:
            if field not in x:
                errors[field] = constants.ERROR_MESSAGE_PREFIX + \
                                constants.READABLE_REQUIRED_FIELDS[field] + \
                                constants.ERROR_MESSAGE_SUFFIX
                valid = False

        # Make sure required boxes checked
        if not ('termsOfService' in x) or not x['termsOfService']:
            errors['termsOfService'] = 'Please read and agree to the rules and code of conduct.'
            valid = False

        # Check if email is valid (basic)
        if 'email' in x and not re.match(constants.EMAIL_MATCH, x['email']):
            errors['email'] = 'Invalid e-mail address.'
            valid = False

        # Check fields with specific values
        choose_one_fields = {
            'gender':constants.GENDERS, 'year':constants.YEARS,
            'shirt':constants.SHIRTS, 'projectType':constants.PROJECTS,
            'travel':constants.TRAVEL_ARRANGEMENTS
        }
        for field in choose_one_fields:
            if field in x and x[field] not in choose_one_fields[field]:
                errors[field] = constants.ERROR_MESSAGE_PREFIX + \
                                constants.READABLE_REQUIRED_FIELDS[field] + \
                                constants.ERROR_MESSAGE_SUFFIX
                valid = False

        if x['travel'] == constants.TRAVEL_ARRANGEMENTS[0]:
            if 'busRoute' not in x or x['busRoute'] == '':
                errors['busRoute'] = constants.ERROR_MESSAGE_PREFIX + \
                                     'Bus Route' + \
                                     constants.ERROR_MESSAGE_SUFFIX
                valid = False

        if 'food' in x and x['food']:
            temp = x['food'].split(',')

            # If answer is Other, user must fill in foodInfo field
            if 'Other' in temp and ('foodInfo' not in x or ('foodInfo' in x and not x['foodInfo'])):
                errors['food'] = constants.ERROR_MESSAGE_PREFIX + \
                                 constants.READABLE_FIELDS['food'] + \
                                 constants.ERROR_MESSAGE_SUFFIX
                valid = False

            for f in x['food'].split(','):
                if f not in constants.FOODS:
                    errors['food'] = constants.ERROR_MESSAGE_PREFIX + \
                                     constants.READABLE_FIELDS['food'] + \
                                     constants.ERROR_MESSAGE_SUFFIX
                    valid = False
                    break

        # ---------- END VALIDATION ----------


        # Create list of error messages separated by '$$$'
        x['errors'] = [ k + '$$$' + errors[k] for k in errors ]

        # Logging based on validity and whether the user is registered already
        if valid:
            x['isRegistered'] = True
            redir = '/apply/complete'
            log_str = 'Signup with email %s' % x['email']

            if db_user and db_user.isRegistered:
                redir = '/apply/updated'
                log_str = 'Updated profile of %s' % x['email']

            logging.info(log_str)
            logging.info(str(x))
        else:
            redir = '/apply'
            logging.info('User with email %s submitted an invalid form', x['email'])
            logging.info(str(errors))

        # Always store the user's data so we can autofill
        # actual registration is determined by the isRegistered flag
        if db_user: success = Attendee.update_search(x, {'userId':x['userId']})
        else: success = Attendee.add(x)

        # TODO check success

        return self.redirect(redir)



class ApplyUpdateHandler(MainHandler.Handler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')

        data = {}
        data['errors'] = {} # Needed for template to render

        data['username'] = user.nickname()
        data['logoutUrl'] = users.create_logout_url('/apply')
        data['email'] = user.email()

        lists = {
            'genders':constants.GENDERS, 'years':constants.YEARS, 'shirts':constants.SHIRTS,
            'foods':constants.FOODS, 'projects':constants.PROJECTS, 'travelArrangements':constants.TRAVEL_ARRANGEMENTS
        }
        for l, options in lists.iteritems(): data[l] = [ {'name':n, 'checked':False} for n in options ]

        data['busRoutes'] = [ {'name':n, 'selected':False} for n in constants.BUS_ROUTES ]

        data['title'] = constants.APPLY_TITLE
        data['hasResume'] = False

        # Check if user is in our database
        db_user = Attendee.search_database({'userId': user.user_id()}).get()
        if db_user:
            if db_user.isRegistered:
                data['isUpdatingApplication'] = True
                data['title'] = constants.PROFILE_TITLE

            # Per-field errors
            # db_user.errors == [<field1>$$$<message1>, <field1>$$$<message2>, ...]
            if db_user.errors:
                # Turn into dictionary so template can do lookup 'data.errors.<field>'
                data['errors'] = { e.split('$$$')[0]:e.split('$$$')[1] for e in db_user.errors }

            text_fields = [
                'nameFirst', 'nameLast', 'email', 'school',
                'experience', 'linkedin', 'github', 'foodInfo',
                'teamMembers'
            ]
            for field in text_fields:
                value = getattr(db_user, field) # Gets db_user.field using a string
                if value: data[field] = value

            choose_one_fields = {
                'gender':('genders','checked'), 'year':('years','checked'),
                'shirt':('shirts','checked'), 'projectType':('projects','selected'),
                'travel':('travelArrangements','checked'), 'busRoute':('busRoutes','selected')
            }
            for field, conn in choose_one_fields.iteritems():
                value = getattr(db_user, field)
                if value:
                    for i in data[conn[0]]:
                        if i['name'] == value:
                            i[conn[1]] = True
                            break

            # Multi-choice check box
            food = db_user.food
            if food:
                for i in data['foods']:
                    if i['name'] in food: i['checked'] = True

            if db_user.resume and db_user.resume.fileName:
                data['hasResume'] = True

            if db_user.termsOfService:
                data['termsOfService'] = True

        data['uploadUrl'] = blobstore.create_upload_url('/apply/update', gs_bucket_name=constants.BUCKET)
        self.render("apply_update.html", data=data)

    def post(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')

        # Initialization
        x = {} # dictionary that will be used to create a new Attendee or update one
        errors = {} # Note: 1 error per field
        valid = True
        db_user = Attendee.search_database({'userId':user.user_id()}).get()

        # Save user information
        # https://developers.google.com/appengine/docs/python/users/userclass
        x['userNickname'] = user.nickname()
        x['userEmail'] = user.email()
        x['userId'] = user.user_id() #use this for identification
        x['userFederatedIdentity'] = user.federated_identity()
        x['userFederatedProvider'] = user.federated_provider()

        x['googleUser'] = user


        # Get data from form
        fields = [
            'nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'experience',
            'linkedin', 'github', 'teamMembers', 'shirt', 'projectType', 'travel', 'busRoute'
        ]
        for field in fields:
           x[field] = self.request.get(field)

        foods = self.request.get_all('food')
        x['food'] = ','.join(foods)
        x['foodInfo'] = self.request.get('foodInfo')

        x['termsOfService'] = (self.request.get('termsOfService') == 'True')
        if not x['termsOfService'] and db_user:
            x['termsOfService'] = db_user.termsOfService


        # Get resume data
        file_info = self.get_file_infos(field_name='resume')
        if file_info and len(file_info) == 1:
            file_info = file_info[0]
            delete_file = False

            # Non-pdf files
            # if not file_info.content_type == 'application/pdf':
            if not file_info.filename[-4:] == '.pdf':
                errors['resume'] = 'Uploaded resume file is not a pdf.'
                delete_file = True
                valid = False

            # Big files
            elif file_info.size > constants.RESUME_MAX_SIZE:
                errors['resume'] = 'Uploaded resume file is too big.'
                delete_file = True
                valid = False

            # Delete uploaded file if appropriate
            if delete_file:
                resource = str(urllib.unquote(file_info.gs_object_name))
                blob_key = blobstore.create_gs_key(resource)
                blobstore.delete(blob_key)

            # Uploaded file is valid, delete old resume if there is one and save new resume
            else:
                # Delete old resume
                if db_user and db_user.resume and db_user.resume.gsObjectName:
                    resource = str(urllib.unquote(db_user.resume.gsObjectName))
                    blob_key = blobstore.create_gs_key(resource)
                    blobstore.delete(blob_key)

                # Save new resume
                x['resume'] = Resume(contentType=file_info.content_type,
                                     creationTime=file_info.creation,
                                     fileName=file_info.filename,
                                     size=file_info.size,
                                     gsObjectName=file_info.gs_object_name)


        # Remove any empty fields from x
        for field in constants.ALL_FIELDS:
            # This checks for None and '' and u''
            if field in x and not x[field]:
                del x[field]


        # ---------- BEGIN VALIDATION ----------

        # Check required fields filled in
        for field in constants.REQUIRED_FIELDS:
            if field not in x:
                errors[field] = constants.ERROR_MESSAGE_PREFIX + \
                                constants.READABLE_REQUIRED_FIELDS[field] + \
                                constants.ERROR_MESSAGE_SUFFIX
                valid = False

        # Make sure required boxes checked
        if not ('termsOfService' in x) or not x['termsOfService']:
            errors['termsOfService'] = 'Please read and agree to the rules and code of conduct.'
            valid = False

        # Check if email is valid (basic)
        if 'email' in x and not re.match(constants.EMAIL_MATCH, x['email']):
            errors['email'] = 'Invalid e-mail address.'
            valid = False

        # Check fields with specific values
        choose_one_fields = {
            'gender':constants.GENDERS, 'year':constants.YEARS,
            'shirt':constants.SHIRTS, 'projectType':constants.PROJECTS,
            'travel':constants.TRAVEL_ARRANGEMENTS
        }
        for field in choose_one_fields:
            if field in x and x[field] not in choose_one_fields[field]:
                errors[field] = constants.ERROR_MESSAGE_PREFIX + \
                                constants.READABLE_REQUIRED_FIELDS[field] + \
                                constants.ERROR_MESSAGE_SUFFIX
                valid = False

        if x['travel'] == constants.TRAVEL_ARRANGEMENTS[0]:
            if 'busRoute' not in x or x['busRoute'] == '':
                errors['busRoute'] = constants.ERROR_MESSAGE_PREFIX + \
                                     'Bus Route' + \
                                     constants.ERROR_MESSAGE_SUFFIX
                valid = False

        if 'food' in x and x['food']:
            temp = x['food'].split(',')

            # If answer is Other, user must fill in foodInfo field
            if 'Other' in temp and ('foodInfo' not in x or ('foodInfo' in x and not x['foodInfo'])):
                errors['food'] = constants.ERROR_MESSAGE_PREFIX + \
                                 constants.READABLE_FIELDS['food'] + \
                                 constants.ERROR_MESSAGE_SUFFIX
                valid = False

            for f in x['food'].split(','):
                if f not in constants.FOODS:
                    errors['food'] = constants.ERROR_MESSAGE_PREFIX + \
                                     constants.READABLE_FIELDS['food'] + \
                                     constants.ERROR_MESSAGE_SUFFIX
                    valid = False
                    break

        # ---------- END VALIDATION ----------


        # Create list of error messages separated by '$$$'
        x['errors'] = [ k + '$$$' + errors[k] for k in errors ]

        # Logging based on validity and whether the user is registered already
        if valid:
            x['isRegistered'] = True
            redir = '/apply/complete'
            log_str = 'Signup with email %s' % x['email']

            if db_user and db_user.isRegistered:
                redir = '/apply/updated'
                log_str = 'Updated profile of %s' % x['email']

            logging.info(log_str)
            logging.info(str(x))
        else:
            redir = '/apply/update'
            logging.info('User with email %s submitted an invalid form', x['email'])
            logging.info(str(errors))

        # Always store the user's data so we can autofill
        # actual registration is determined by the isRegistered flag
        if db_user: success = Attendee.update_search(x, {'userId':x['userId']})
        else: success = Attendee.add(x)

        # TODO check success

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

        if not user: return self.abort(500, detail='User not logged in')

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
