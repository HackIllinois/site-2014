from google.appengine.ext import db

''' Test Script
from db import db
from db import models
import datetime as dt

a = models.Attendee.new('Alex', 'Burck', 'burck1@illinois.edu', 3)
a.isAdmin = True
a.isParticipant = False
a.put() # don't forget this

t = models.Team.new('Test')
t.put()
t.addMember(a)
t.put()

s = models.Sponsor.new('Test Company', 'Qwerty Uiop', 'qwerty@company.com')
s.put()
n = models.Note.new('burck1@illinois.edu', 'qwerty@company.com', dt.datetime.now(), 'Test', 'Test')
n.put()
s.addNote(n)
s.put()
'''

def _get_required(cls):
    '''
    private method for getting a list of all required properties of a class
    '''
    properties = cls.properties()
    required = []
    for p in properties:
        if properties[p].required:
            required.append(p)
    return required


def add(cls, data):
    '''
    Creates a model and adds it to the database
    WILL NOT override data if already there

    @param cls: the class model to use
    @param data: the data to add in the database
    @return: whether or not the data was added to the database

    ex: add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'standing':3})
    '''
    cls.new(data).put()
    # TODO: add check if already in database
    return True

def update(cls, search, data):
    '''
    Creates a model and adds it to the database
    WILL override data if already there

    @param cls: the class model to use
    @param search: the parameters to search with
    @param data: the data to change in the database
    @return: whether or not the data was found in the database

    ex: update(Attendee, {'nameFirst':'John', 'nameLast':'Doe'}, {'email':'doe1@illinois.edu', 'standing':3})
    '''
    pass

def add_or_update(cls, data):
    if not add(cls, data):
        required = _get_required(cls)
        search = {}
        for r in required:
            if r in data:
                search[r] = data[r]
                del data[r]
        update(cls, search, data)


class Attendee(db.Model):
    nameFirst = db.StringProperty(required=True)
    nameLast = db.StringProperty(required=True)
    isAdmin = db.BooleanProperty(default=False) #Set Default to False
    isParticipant = db.BooleanProperty(default=False) #Set Default to False
    email = db.EmailProperty(required=True)
    standing = db.IntegerProperty(choices=[0,1,2,3,4,5]) # 0=fresh, 1=soph, 2=jr, 3=sr, 4=grad, 5=other
    registrationTime = db.DateTimeProperty(auto_now_add=True)
    team = db.Key()

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        attendee = cls(nameFirst='PlaceHolder', nameLast='PlaceHolder', email='PlaceHolder')
        for k in data:
            setattr(attendee, k, data[k])
        return attendee

    @classmethod
    def new2(cls, mNameFirst, mNameLast, mEmail, mStanding):
        return cls(nameFirst=mNameFirst, nameLast=mNameLast, email=mEmail, standing=mStanding)


class Team(db.Model):
    name = db.StringProperty(required=True)
    teamMembers = db.ListProperty(type(db.Key()))

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(name='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def new2(cls, mName):
        return cls(name=mName)

    def addMember(self, person):
        if type(person) == Attendee:
            self.teamMembers.append(person.key())
            person.team = self.key()
        return type(person) == Attendee


class Note(db.Model):
    emailTo = db.EmailProperty(required=True)
    emailFrom = db.EmailProperty(required=True)
    dateTime = db.DateTimeProperty(required=True)
    subject = db.StringProperty()
    text = db.StringProperty(required=True)

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(emailTo='PlaceHolder', emailFrom='PlaceHolder', dateTime='PlaceHolder', text='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def new2(cls, mEmailTo, mEmailFrom, mDateTime, mSubject, mText):
        return cls(emailTo=mEmailTo, emailFrom=mEmailFrom, dateTime=mDateTime, subject=mSubject, text=mText)

class Sponsor(db.Model):
    companyName = db.StringProperty(required=True)
    contactName = db.StringProperty()
    email = db.EmailProperty(required=True)
    levelOfSponsorship = db.IntegerProperty()
    notes = db.ListProperty(type(db.Key()))

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(companyName='PlaceHolder', emailFrom='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def new2(cls, mCompanyName, mContactName, mEmail):
        return cls(companyName=mCompanyName, contactName=mContactName, email=mEmail)

    def addNote(self, note):
        if type(note) == Note:
            self.notes.append(note.key())
        return type(note) == Note

class SignUp(db.Model):
    """ Emails collected before launching the full site """
    email = db.StringProperty(required=True)
    register_date = db.DateProperty()