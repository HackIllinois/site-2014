from google.appengine.ext import ndb
import datetime as dt

''' Test Script
import os
import pprint

from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from db import db
from db import models
import datetime as dt

data = {'nameFirst':'Alex', 'nameLast':'Burck', 'email':'burck1@illinois.edu', 'standing':4}
me = models.add(models.Attendee, data)

data = {'name':'Test'}
t = models.add(models.Team, data)
t.addMember(me)

data = {'companyName':'Test Company', 'contactName':'Qwerty Uiop', 'email':'qwerty@company.com'}
s = models.add(models.Sponsor, data)

data = {'emailTo':'burck1@illinois.edu', 'emailFrom':'qwerty@company.com', 'dateTime':dt.datetime.now(), 'subject':'Test', 'text':'Test'}
n = models.add(models.Note, data)
s.addNote(n)
'''

def _get_required(cls):
    '''
    private method for getting a list of all required properties of a class
    '''
    properties = cls._properties
    required = []
    for p in properties:
        if properties[p]._required:
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
    o = cls.new(data)
    o.put()
    # TODO: add check if already in database
    return o

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


class Attendee(ndb.Model):
    nameFirst = ndb.StringProperty(required=True)
    nameLast = ndb.StringProperty(required=True)
    isAdmin = ndb.BooleanProperty(default=False) #Set Default to False
    isParticipant = ndb.BooleanProperty(default=False) #Set Default to False
    email = ndb.StringProperty(required=True)
    standing = ndb.IntegerProperty(choices=[0,1,2,3,4,5]) # 0=fresh, 1=soph, 2=jr, 3=sr, 4=grad, 5=other
    registrationTime = ndb.DateTimeProperty(auto_now_add=True)
    team = ndb.KeyProperty()

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


class Team(ndb.Model):
    name = ndb.StringProperty(required=True)
    teamMembers = ndb.StructuredProperty(Attendee, repeated=True)

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
            self.teamMembers.append(person)
            person.team = self.key
            self.put()
            person.put()
        return type(person) == Attendee


class Note(ndb.Model):
    emailTo = ndb.StringProperty(required=True)
    emailFrom = ndb.StringProperty(required=True)
    dateTime = ndb.DateTimeProperty(required=True)
    subject = ndb.StringProperty()
    text = ndb.TextProperty(required=True)

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(emailTo='PlaceHolder', emailFrom='PlaceHolder', dateTime=dt.datetime.now(), text='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def new2(cls, mEmailTo, mEmailFrom, mDateTime, mSubject, mText):
        return cls(emailTo=mEmailTo, emailFrom=mEmailFrom, dateTime=mDateTime, subject=mSubject, text=mText)

class Sponsor(ndb.Model):
    companyName = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    levelOfSponsorship = ndb.IntegerProperty()
    notes = ndb.StructuredProperty(Note, repeated=True)

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(companyName='PlaceHolder', email='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def new2(cls, mCompanyName, mContactName, mEmail):
        return cls(companyName=mCompanyName, contactName=mContactName, email=mEmail)

    def addNote(self, note):
        if type(note) == Note:
            self.notes.append(note)
            self.put()
        return type(note) == Note

class SignUp(ndb.Model):
    """ Emails collected before launching the full site """
    email = ndb.StringProperty(required=True)
    register_date = ndb.DateProperty()