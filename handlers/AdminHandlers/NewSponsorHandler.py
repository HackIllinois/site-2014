import MainAdminHandler
import urllib
from db.Sponsor import Sponsor
from db import constants
import json
import random

def csv_split_and_validate(orig_str):
    out = orig_str.strip()
    if not out: return None
    out = re.split(r'[,; \n]', out)
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
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to create sponsors.')

        companyName = str(urllib.unquote(self.request.get('companyName')))
	    email = str(urllib.unquote(self.request.get('email')))
	    name = str(urllib.unquote(self.request.get('name')))
	    jobTitle = str(urllib.unquote(self.request.get('jobTitle')))

	    skills = str(urllib.unquote(self.request.get('skills')))
	    skills = csv_split_and_validate(skills)

	    status_list = str(urllib.unquote(self.request.get('status_list')))
	    status_list = csv_split_and_validate(status_list)
	    
	    database_key = get_next_sponsor_key()
