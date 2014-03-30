import MainAdminHandler
import urllib, logging
from db.Attendee import Attendee
from db import constants

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class ProfileHandler(MainAdminHandler.BaseAdminHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self, userId):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendee profiles.')

        userId = str(urllib.unquote(userId))
        db_user = Attendee.search_database({'userId':userId}).get()
        # TODO: add sanity check for user exists

        data = {}
        text_fields = [
            'nameFirst', 'nameLast', 'email', 'school',
            'experience', 'linkedin', 'github', 'year',
            'gender', 'projectType', 'shirt', 'food',
            'foodInfo', 'teamMembers', 'registrationTime',
            'userNickname', 'userEmail', 'userId', 'isApproved',
            'travel', 'busRoute', 'resume', 'approvalStatus']

        for field in text_fields:
            value = getattr(db_user, field) # Gets db_user.field using a string
            if value is not None: data[field] = value

        if db_user.resume and db_user.resume.fileName:
            data['hasResume'] = True

        lists = {
            'genders':constants.GENDERS, 'years':constants.YEARS, 'shirts':constants.SHIRTS,
            'foods':constants.FOODS, 'projects':constants.PROJECTS, 'schools':constants.SCHOOLS
        }
        for l, options in lists.iteritems(): data[l] = [ n for n in options ]

        data['status'] = db_user.approvalStatus.status if db_user.approvalStatus is not None else None

        return self.render("admin_profile.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)



    def post(self, userId):

        db_user = Attendee.search_database({'userId':userId}).get()
        x = {} # dictionary that will be used to create a new Attendee or update one
        errors = {} # Note: 1 error per field
        valid = True

        fields = ['nameFirst', 'nameLast', 'gender', 'school', 'year', 'experience',
            'linkedin', 'github', 'teamMembers', 'shirt', 'projectType', 'food', 'foodInfo']
        for field in fields:
            x[field] = self.request.get(field)

    #    foods = self.request.get_all('foodCheck')
     #   x['food'] = ','.join(foods)

        """
        # Get resume data
        file_info = self.get_file_infos('resumeInput')
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
        """

        # Replace any empty fields from x
        all_fields = constants.ALL_FIELDS.append('teamMembers')#Remove once constants.ALL_FIELDS is updated
        for field in constants.ALL_FIELDS:
            # This checks for '' and u''
            if field in x and not x[field]:
                x[field] = None


        # ---------- BEGIN VALIDATION ----------

        # Check required fields filled in
        req_fields = constants.REQUIRED_FIELDS
        if 'email' in req_fields:
            req_fields.remove('email')
        for field in req_fields:
            if field not in x or not x[field]:
                logging.error(field)
                errors[field] = constants.ERROR_MESSAGE_PREFIX + \
                                constants.READABLE_REQUIRED_FIELDS[field] + \
                                constants.ERROR_MESSAGE_SUFFIX
                valid = False

        # Check fields with specific values
        choose_one_fields = {
            'gender':constants.GENDERS, 'year':constants.YEARS,
            'shirt':constants.SHIRTS, 'projectType':constants.PROJECTS
        }
        for field in choose_one_fields:
            if field in x and x[field] not in choose_one_fields[field]:
                errors[field] = constants.ERROR_MESSAGE_PREFIX + \
                                constants.READABLE_REQUIRED_FIELDS[field] + \
                                constants.ERROR_MESSAGE_SUFFIX
                valid = False

        if 'food' in x and x['food']:
            temp = x['food'].split(',')

            # If answer is Other, user must fill in foodInfo field
            if 'Other' in temp and ('foodInfo' not in x or ('foodInfo' in x and not x['foodInfo'])):
                errors['food-specific'] = constants.ERROR_MESSAGE_PREFIX + \
                                 constants.READABLE_FIELDS['food-info'] + \
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
            if db_user:  Attendee.update_search(x, {'userId':userId})
            else: return self.write("Error: Attendee dosn't excist")
            return self.write("Edit Complete")
        else:
            logging.error(str(errors))
            return self.write("Error: Invalid Data: " + str(errors))
