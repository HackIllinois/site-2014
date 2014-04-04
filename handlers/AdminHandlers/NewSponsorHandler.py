import MainAdminHandler
import urllib
from db.Sponsor import Sponsor
from db import constants
import json
import re
import random
from datetime import datetime

def csv_split_and_validate(orig_str):
    out = orig_str.strip()
    if not out: return None
    out = re.split(r'[,;]', out)
    out = [ i.strip() for i in out ]
    return out

def get_next_sponsor_key():
    key = None
    while not key:
        i = random.randint(constants.SPONSOR_START_COUNT, constants.SPONSOR_START_COUNT+9998)
        c = Sponsor.search_database({'database_key':i}).count()
        if c == 0: key = i
    return key

class NewSponsorHandler(MainAdminHandler.BaseAdminHandler):
    def post(self):
        """Keys
        email: Required: String
        companyName: Required if new: String
        name: Required if new: String
        jobTitle: Required if new: String
        skills: Not Required: comma/semi-colon separated list
        status_list: Not Required: comma/semi-colon separated list
        """

        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to create sponsors.')

        email = str(urllib.unquote(self.request.get('email')))
        if not email:
            return self.write("Error: No 'email' key given\n")

        if not re.match(constants.EMAIL_MATCH, email):
            return self.write("Error: Invalid 'email' given\n")

        valid = True
        db_sponsor = Sponsor.search_database({'email':email}).get()

        companyName = str(urllib.unquote(self.request.get('companyName')))
        if db_sponsor and companyName:
            db_sponsor.companyName = companyName
        elif not companyName:
            valid = False
            self.write("Error: No 'companyName' key given\n")

        name = str(urllib.unquote(self.request.get('name')))
        if db_sponsor and name:
            db_sponsor.name = name
        elif not name:
            valid = False
            self.write("Error: No 'name' key given\n")

        jobTitle = str(urllib.unquote(self.request.get('jobTitle')))
        if db_sponsor and jobTitle:
            db_sponsor.jobTitle = jobTitle
        elif not jobTitle:
            valid = False
            self.write("Error: No 'jobTitle' key given\n")

        if not valid: return

        updatedTime = datetime.now()
        if db_sponsor: db_sponsor.updatedTime = updatedTime

        skills = str(urllib.unquote(self.request.get('skills')))
        skills = csv_split_and_validate(skills)
        if db_sponsor and skills:
            db_sponsor.skills = skills

        status_list = str(urllib.unquote(self.request.get('status_list')))
        status_list = csv_split_and_validate(status_list)
        if db_sponsor and status_list:
            db_sponsor.status_list = status_list
        
        
        if db_sponsor:
            db_sponsor.put()
            self.write("Sponsor %s successfully updated" % email)
        else:
            database_key = get_next_sponsor_key()
            Sponsor(
                parent=Sponsor.get_default_event_parent_key(),
                companyName=companyName,
                email=email,
                name=name,
                jobTitle=jobTitle,
                updatedTime=updatedTime,
                skills=skills,
                status_list=status_list,
                database_key=database_key
            ).put()
            self.write("Sponsor %s successfully created" % email)

        return
