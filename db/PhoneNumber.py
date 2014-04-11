from google.appengine.ext import ndb
from Model import Model

class PhoneNumber(Model):
    Model._automatically_add_event_as_ancestor()

    number = ndb.StringProperty()

    # Access Groups
    # Staff = on recieve text message list for staff
    # SendStaff = on send text message list for staff
    groups = ndb.StringProperty(repeated=True)

    creationTime = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def new(cls, data):
        number = cls()
        for k in data:
            setattr(number, k, data[k])
        return number
