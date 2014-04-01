from google.appengine.ext import ndb
import constants
from Model import Model
from db.Attendee import Attendee
from db.Email import Email

class Group(Model):
    Model._automatically_add_event_as_ancestor()

    groupNumber = ndb.IntegerProperty()

    firstEmail = ndb.StructuredProperty(Email)
    secondEmail = ndb.StructuredProperty(Email)
    thirdEmail = ndb.StructuredProperty(Email)

    closingTime = ndb.DateTimeProperty()

    people = KeyProperty(kind=Attendee, repeated=True)

    @classmethod
    def new(cls, data):
        group = cls()
        for k in data:
            setattr(group, k, data[k])
        return group
