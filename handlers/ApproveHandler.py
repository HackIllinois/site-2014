import MainHandler
import db.models as models
from google.appengine.ext import blobstore
import cloudstorage as gcs
from google.appengine.api import files

class ApproveHandler(MainHandler.Handler):

    def get(self):
        ## @TODO: login implementation

        db_all_users = models.search_database(models.Attendee, {})

        if db_all_users is None:
            self.response.out.write('ERROR') # @TODO: implement error handling here
        else:
            all_users = db_all_users.fetch(10)
            
            for user in all_users:
                resume_url = "/blobstore/hackillinois/" + user.resumePath
                
                blob_key = files.blobstore.get_blob_key(resume_url)
                blob_reader = blobstore.BlobReader(blob_key)
                print blob_reader.read()

                #print blobstore.BlobInfo.get(blob_key)

            self.render('approve.html', all_users=all_users)