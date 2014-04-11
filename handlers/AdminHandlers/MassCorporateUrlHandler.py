import MainAdminHandler
from db.Admin import Admin
from db.CorporateUrl import CorporateUrl

import random
import json

class MassCorporateUrlHandler(MainAdminHandler.BaseAdminHandler):

    def get(self):
      admin_user = self.get_admin_user()
      if not admin_user: return self.abort(500, detail='User not in database')
      if not admin_user.corporateAdminAccess:
          return self.abort(401, detail='User does not have permission to create corporate urls.')
      urls = []
      for url in self.request.get('size'):
        # http://stackoverflow.com/questions/2782229/most-lightweight-way-to-create-a-random-string-and-a-random-hexadecimal-number
        uniqueString = '%05x' % random.randrange(16**5)

        while CorporateUrl.search_database({'uniqueString': uniqueString}).get() is not None:
            uniqueString = '%05x' % random.randrange(16**5)

        access = self.request.get('attendeeDataAccess') == 'True'

        CorporateUrl.add({'uniqueString': uniqueString, 'attendeeDataAccess': access})

        urls.append(self.request.host_url+'/c-registration/'+uniqueString)
      return self.write(urls)