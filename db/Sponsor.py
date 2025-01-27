from google.appengine.ext import ndb
import constants
from Model import Model
from Task import Task
import json

class Sponsor(Model):
    Model._automatically_add_event_as_ancestor()

    # https://developers.google.com/appengine/docs/python/users/userclass
    # .nickname(), .email(), .user_id()
    googleUser = ndb.UserProperty()

    # For user object look at https://developers.google.com/appengine/docs/python/users/userclass
    '''These are all computed from the googleUser property'''
    userNickname = ndb.ComputedProperty(lambda self: self.googleUser.nickname())
    userEmail = ndb.ComputedProperty(lambda self: self.googleUser.email())
    userId = ndb.ComputedProperty(lambda self: self.googleUser.user_id())
    '''These are all computed from the googleUser property'''

    # these vairables are needed for mobile
    # Note: this is the email that hackers will use to contact the sponsor
    email = ndb.StringProperty(default='')
    companyName = ndb.StringProperty(default='')
    name = ndb.StringProperty(default='')
    jobTitle = ndb.TextProperty(default='')

    skills = ndb.JsonProperty(default=[''])
    status = ndb.TextProperty(default='')
    pictureURL = ndb.TextProperty(default='')
    homebase = ndb.TextProperty(default='')
    updatedTime = ndb.IntegerProperty()
    email_lower = ndb.ComputedProperty(lambda self: self.email.lower())
    database_key = ndb.IntegerProperty(default=0)
    status_list = ndb.JsonProperty(default=[])
    personType = 'mentor'
    mac_address = ndb.StringProperty(default='')

    task_queue = ndb.KeyProperty(kind=Task, repeated=True)

    attendeeDataAccess = ndb.BooleanProperty(default=False)

    access = ndb.ComputedProperty(lambda self: json.dumps({ 'attendeeData':self.attendeeDataAccess, }))

    @classmethod
    def new(cls, data):
        sponsor = cls()
        for k in data:
            setattr(sponsor, k, data[k])
        return sponsor
