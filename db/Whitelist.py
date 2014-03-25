from google.appengine.ext import ndb
from Model import Model
import constants

class Whitelist(Model):
    Model._automatically_add_event_as_ancestor()

    uniqueString = ndb.StringProperty()
    enabled = ndb.BooleanProperty(default=True)

    intendedRecipientEmail = ndb.StringProperty()
    userEmail = ndb.StringProperty()
    userId = ndb.StringProperty()

    creationTime = ndb.DateTimeProperty(auto_now_add=True)
    registerTime = ndb.DateTimeProperty()

    @classmethod
    def new(cls, data):
        admin = cls()
        for k in data:
            setattr(admin, k, data[k])
        return admin
