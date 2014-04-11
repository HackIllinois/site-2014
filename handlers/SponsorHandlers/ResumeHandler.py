import MainSponsorHandler
from db.Attendee import Attendee

import urllib

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class ResumeHandler(MainSponsorHandler.BaseSponsorHandler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
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
