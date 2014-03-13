from google.appengine.ext import ndb
from Model import Model
import constants

class CompanyRep(Model):
    Model._automatically_add_event_as_ancestor()

    email = ndb.StringProperty()
    googleUser = ndb.UserProperty()
    company = ndb.StringProperty()

    jobTitle = ndb.TextProperty()
    skills = ndb.TextProperty()
    officeHours = ndb.TextProperty()
    programmingLanguages = ndb.TextProperty()
    frameworkAndAPI = ndb.TextProperty()

    # For people who have access to approve and disapprove attendees
    approveAccess = ndb.BooleanProperty(default=False)

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


#name: ,company: ,job title: ,skills: ,events: ,office hours: ,email/contact: 