from google.appengine.ext import ndb
from Model import Model

class Resume(Model):
    # https://developers.google.com/appengine/docs/python/blobstore/fileinfoclass
    contentType = ndb.StringProperty()
    creationTime = ndb.DateTimeProperty()
    fileName = ndb.StringProperty()
    size = ndb.IntegerProperty() # in Bytes
    gsObjectName = ndb.StringProperty()

    @classmethod
    def new(cls, data):
        resume = cls()
        for k in data:
            setattr(resume, k, data[k])
        return resume

    @classmethod
    def unique_properties(cls):
        return ['gsObjectName']
