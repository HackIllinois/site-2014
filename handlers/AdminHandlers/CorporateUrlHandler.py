import MainAdminHandler
from db.Admin import Admin
from db.CorporateUrl import CorporateUrl

import random
import json

class CorporateUrlHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.corporateAdminAccess:
            return self.abort(401, detail='User does not have permission to create corporate urls.')

        data = {}

        db_urls = CorporateUrl.search_database({}).order(-CorporateUrl.creationTime)
        urls = [ {'enabled': u.enabled,
                  'attendeeDataAccess': u.attendeeDataAccess,
                  'url': self.request.host_url+'/c-registration/'+u.uniqueString,
                  'creationTime': u.creationTime.strftime('%x %X'),
                  'userEmail': u.googleUser.email() if u.googleUser else None,
                  'registerTime': u.registerTime.strftime('%x %X') if u.registerTime else None
                 } for u in db_urls ]
        data['urls'] = urls
        return self.render('admin_corporate.html', data=data, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.corporateAdminAccess:
            return self.abort(401, detail='User does not have permission to create corporate urls.')

        # http://stackoverflow.com/questions/2782229/most-lightweight-way-to-create-a-random-string-and-a-random-hexadecimal-number
        uniqueString = '%05x' % random.randrange(16**5)

        while CorporateUrl.search_database({'uniqueString': uniqueString}).get() is not None:
            uniqueString = '%05x' % random.randrange(16**5)

        access = self.request.get('attendeeDataAccess') == 'True'

        CorporateUrl.add({'uniqueString': uniqueString, 'attendeeDataAccess': access})

        return self.write(self.request.host_url+'/c-registration/'+uniqueString)
