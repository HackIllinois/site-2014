import MainAdminHandler
from db.Attendee import Attendee

import urllib

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class ResumeHandler(MainAdminHandler.BaseAdminHandler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendee resumes.')

        userId = str(urllib.unquote(self.request.get('userId')))
        db_user = Attendee.search_database({'userId':userId}).get()
        if not db_user:
            return self.render( "simple_message.html",
                                header="Not Available",
                                message="User ID is not valid.",
                                showSocial=False )

        if not db_user.resume:
            return self.render( "simple_message.html",
                                header="Not Available",
                                message="User has not uploaded a resume.",
                                showSocial=False )

        # https://developers.google.com/appengine/docs/python/blobstore/#Python_Using_the_Blobstore_API_with_Google_Cloud_Storage
        resource = str(urllib.unquote(db_user.resume.gsObjectName))
        blob_key = blobstore.create_gs_key(resource)
        return self.send_blob(blob_key)