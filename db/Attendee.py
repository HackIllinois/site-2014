from google.appengine.ext import ndb
import constants
from Resume import Resume
from Model import Model
from google.appengine.ext.db import BadValueError

class Attendee(Model):
    # This is the workaround for the strong consistency
    Model._automatically_add_event_as_ancestor()

    # For user object look at https://developers.google.com/appengine/docs/python/users/userclass
    userNickname = ndb.StringProperty()
    userEmail = ndb.StringProperty()
    userId = ndb.StringProperty()
    userFederatedIdentity = ndb.StringProperty()
    userFederatedProvider = ndb.StringProperty()

    nameFirst = ndb.StringProperty(required=True)
    nameLast = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    gender = ndb.StringProperty(choices=constants.GENDERS)
    school = ndb.StringProperty()
    year = ndb.StringProperty(choices=constants.YEARS)

    experience = ndb.TextProperty() # unlimited length, not indexed
    resume = ndb.StructuredProperty(Resume)
    linkedin = ndb.StringProperty()
    github = ndb.StringProperty()

    shirt = ndb.StringProperty(choices=constants.SHIRTS)
    # food = ndb.StringProperty(choices=constants.FOODS)
    food = ndb.StringProperty()
    foodInfo = ndb.TextProperty()

    teamMembers = ndb.TextProperty()
    projectType = ndb.StringProperty(choices=constants.PROJECTS)
    userNotes = ndb.TextProperty()

    recruiters = ndb.BooleanProperty(default=False)
    picture = ndb.BooleanProperty(default=False)
    termsOfService = ndb.BooleanProperty(default=False)

    isAdmin = ndb.BooleanProperty(default=False)
    isParticipant = ndb.BooleanProperty(default=False)

    isRegistered = ndb.BooleanProperty(default=False)
    registrationTime = ndb.DateTimeProperty(auto_now_add=True)

    applyError = ndb.BooleanProperty()
    errorMessages = ndb.TextProperty()

    approved = ndb.StringProperty()

    team = ndb.KeyProperty()

    @classmethod
    def new(cls, data):
        required = cls._get_required()
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        attendee = cls(nameFirst='PlaceHolder', nameLast='PlaceHolder', email='PlaceHolder')
        for k in data:
            setattr(attendee, k, data[k])
        return attendee

    @classmethod
    def unique_properties(cls):
        return ['email']

    @classmethod
    def new2(cls, mNameFirst, mNameLast, mEmail, mYear):
        return cls(nameFirst=mNameFirst, nameLast=mNameLast, email=mEmail, year=mYear)