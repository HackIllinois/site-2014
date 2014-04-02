from google.appengine.ext import ndb
from Model import Model
import constants

class Admin(Model):
    Model._automatically_add_event_as_ancestor()

    email = ndb.StringProperty()
    googleUser = ndb.UserProperty()

    # these vairables are needed for mobile
    userId = ndb.StringProperty(default='')
    name = ndb.StringProperty(default='')
    school = ndb.TextProperty(default='')
    year = ndb.TextProperty(default='')
    homebase = ndb.TextProperty(default='')
    skills = ndb.JsonProperty(default=[''])
    status = ndb.TextProperty(default='')
    updatedTime = ndb.StringProperty(default='')
    pictureURL= ndb.TextProperty(default='')
    email_lower = ndb.ComputedProperty(lambda self: self.email.lower())
    companyName = ndb.StringProperty(default='HackIllinois')
    jobTitle = ndb.TextProperty(default='')
    database_key = ndb.IntegerProperty(default=0)
    status_list = ndb.JsonProperty(default=[])


    # For people who have access to approve and disapprove attendees
    approveAccess = ndb.BooleanProperty(default=False)

    # For people who have access to change mobile things
    mobileAccess = ndb.BooleanProperty(default=False)

    # Only Systems-Core and Matthew have this
    fullAccess = ndb.BooleanProperty(default=False)

    @classmethod
    def new(cls, data):
        admin = cls()
        for k in data:
            setattr(admin, k, data[k])
        return admin

    @classmethod
    def unique_properties(cls):
        return ['email']
