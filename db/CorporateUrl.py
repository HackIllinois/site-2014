from google.appengine.ext import ndb
from Model import Model
import constants
import hashlib

class CorporateUrl(Model):
    Model._automatically_add_event_as_ancestor()

    uniqueString = ndb.StringProperty()

    enabled = ndb.BooleanProperty(default=True)
    attendeeDataAccess = ndb.BooleanProperty(default=False)

    # https://developers.google.com/appengine/docs/python/users/userclass
    # .nickname(), .email(), .user_id()
    # This is set once a user logs in with the unique url
    googleUser = ndb.UserProperty()

    creationTime = ndb.DateTimeProperty(auto_now_add=True)
    registerTime = ndb.DateTimeProperty()

    @classmethod
    def new(cls, data):
        url = cls()
        for k in data:
            setattr(url, k, data[k])
        return url
