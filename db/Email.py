from google.appengine.ext import ndb
import constants
from Model import Model

class Email(Model):
    Model._automatically_add_event_as_ancestor()

    sent = ndb.BooleanProperty(default=False)
    sentTime = ndb.DateTimeProperty()
    sentBy = ndb.StringProperty()
    note = ndb.TextProperty()

    @classmethod
    def new(cls, data):
        email = cls()
        for k in data:
            setattr(email, k, data[k])
        return email
