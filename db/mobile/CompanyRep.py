from google.appengine.ext import ndb
from db.Model import Model
from db import constants

class CompanyRep(Model):
    Model._automatically_add_event_as_ancestor()

    email = ndb.StringProperty()
    googleUser = ndb.UserProperty()
    company = ndb.StringProperty()

    jobTitle = ndb.TextProperty()
    skills = ndb.JsonProperty()
    status = ndb.TextProperty()

    @classmethod
    def new(cls, data):
        companyRep = cls()
        for k in data:
            setattr(companyRep, k, data[k])
        return companyRep

    @classmethod
    def unique_properties(cls):
        return ['email']