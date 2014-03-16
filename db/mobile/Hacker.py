from google.appengine.ext import ndb
from db.Model import Model
from db import constants

class Hacker(Model):
    Model._automatically_add_event_as_ancestor()

    email = ndb.StringProperty()
    googleUser = ndb.UserProperty()
    userId = ndb.StringProperty()


    name = ndb.StringProperty()
    school = ndb.TextProperty()
    year = ndb.TextProperty()
    skills = ndb.JsonProperty()
    homebase = ndb.TextProperty()

    @classmethod
    def new(cls, data):
        hacker = cls()
        for k in data:
            setattr(hacker, k, data[k])
        return hacker

    @classmethod
    def unique_properties(cls):
        return ['email']