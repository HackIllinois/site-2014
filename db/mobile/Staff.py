from google.appengine.ext import ndb
from db.Model import Model
from db import constants

class Staff(Model):
    Model._automatically_add_event_as_ancestor()

    email = ndb.StringProperty()
    googleUser = ndb.UserProperty()
    userId = ndb.StringProperty()

    name = ndb.StringProperty()
    school = ndb.TextProperty()
    year = ndb.TextProperty()
    homebase = ndb.TextProperty()
    skills = ndb.JsonProperty()

    @classmethod
    def new(cls, data):
        staff = cls()
        for k in data:
            setattr(staff, k, data[k])
        return staff

    @classmethod
    def unique_properties(cls):
        return ['email']