from google.appengine.ext import ndb
import constants
from Model import Model

class Sponsor(Model):
    companyName = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    levelOfSponsorship = ndb.StringProperty()
    initialId = ndb.StringProperty()
    initialLogin = ndb.BooleanProperty()
    userId = ndb.StringProperty()
    googleUser = ndb.UserProperty()

    # these vairables are needed for mobile
    name = ndb.StringProperty(default='')
    jobTitle = ndb.TextProperty(default='')
    skills = ndb.JsonProperty(default=[''])
    status = ndb.TextProperty(default='')
    pictureURL = ndb.TextProperty(default='')
    name = ndb.StringProperty(default='', required=True)
    updatedTime = ndb.DateTimeProperty()
    email_lower = ndb.ComputedProperty(lambda self: self.email.lower())
    database_key = ndb.IntegerProperty(default=0)
    status_list = ndb.JsonProperty()



    @classmethod
    def new(cls, data):
        sponsor = cls()
        for k in data:
            setattr(sponsor, k, data[k])
        return sponsor