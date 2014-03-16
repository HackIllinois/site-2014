from google.appengine.ext import ndb
import constants
from Model import Model
from google.appengine.ext.db import BadValueError

class Sponsor(Model):
    companyName = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    levelOfSponsorship = ndb.StringProperty()
    initialId = ndb.StringProperty()
    initialLogin = ndb.BooleanProperty()
    userId = ndb.StringProperty()

    @classmethod
    def new(cls, data):
        sponsor = cls()
        for k in data:
            setattr(sponsor, k, data[k])
        return sponsor