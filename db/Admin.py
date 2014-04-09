from google.appengine.ext import ndb
from Model import Model
import constants

import json

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

    statsAccess = ndb.BooleanProperty(default=False)
    approveAccess = ndb.BooleanProperty(default=False)
    approveAdminAccess = ndb.BooleanProperty(default=False)
    mobileAccess = ndb.BooleanProperty(default=False)
    corporateAdminAccess = ndb.BooleanProperty(default=False)
    managerAccess = ndb.BooleanProperty(default=False)
    # personType = 'Staff'

    access = ndb.ComputedProperty(lambda self: json.dumps({ 'stats':self.statsAccess,
                                                            'approve':self.approveAccess,
                                                            'approveAdmin':self.approveAdminAccess,
                                                            'mobile':self.mobileAccess,
                                                            'corporate':self.corporateAdminAccess,
                                                            'manager':self.managerAccess }))

    @classmethod
    def new(cls, data):
        admin = cls()
        for k in data:
            setattr(admin, k, data[k])
        return admin

    @classmethod
    def unique_properties(cls):
        return ['email']
