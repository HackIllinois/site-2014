from google.appengine.ext import ndb
import constants
from Model import Model

class Status(Model):
    Model._automatically_add_event_as_ancestor()

    status = ndb.StringProperty(choices=constants.STATUSES, default='Not Approved')

    approvedTime = ndb.DateTimeProperty()
    waitlistedTime = ndb.DateTimeProperty()
    rsvpTime = ndb.DateTimeProperty()

    @classmethod
    def new(cls, data):
        status = cls()
        for k in data:
            setattr(status, k, data[k])
        return status
