from google.appengine.ext import ndb
import datetime as dt

'''
NDB cheatsheet: https://docs.google.com/document/d/1AefylbadN456_Z7BZOpZEXDq8cR8LYu7QgI7bt5V0Iw/edit#

To run all unit tests:

from pprint import pprint
from db import models
ut = models.UnitTest()
pprint(ut.run_all())

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



class UnitTest(object):
    ''' To run all unit tests:
    from pprint import pprint
    from db import models
    ut = models.UnitTest()
    pprint(ut.run_all())
    '''
    import sys

    def test_add_attendee(self):
        passed = True
        data = {'nameFirst':'Alex', 'nameLast':'Burck', 'email':'burck1@illinois.edu', 'standing':4}
        try:
            me = add(Attendee, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed


    def test_add_team(self):
        passed = True
        data = {'name':'Test'}
        try:
            t = add(Team, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_attendee_to_team(self):
        passed = True
        data = {'nameFirst':'Alex', 'nameLast':'Burck', 'email':'burck1@illinois.edu', 'standing':4}
        me = add(Attendee, data)
        data = {'name':'Test'}
        t = add(Team, data)
        try:
            passed = t.addMember(me)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_sponsor(self):
        passed = True
        data = {'companyName':'Test Company', 'contactName':'Qwerty Uiop', 'email':'qwerty@company.com'}
        try:
            s = add(Sponsor, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_note(self):
        passed = True
        data = {'emailTo':'burck1@illinois.edu', 'emailFrom':'qwerty@company.com', 'dateTime':dt.datetime.now(), 'subject':'Test', 'text':'Test'}
        try:
            n = add(Note, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_note_to_sponsor(self):
        passed = True
        data = {'companyName':'Test Company', 'contactName':'Qwerty Uiop', 'email':'qwerty@company.com'}
        s = add(Sponsor, data)
        data = {'emailTo':'burck1@illinois.edu', 'emailFrom':'qwerty@company.com', 'dateTime':dt.datetime.now(), 'subject':'Test', 'text':'Test'}
        n = add(Note, data)
        try:
            passed = s.addNote(n)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def run_all(self):
        tests = { self.test_add_attendee:'Add Attendee',
                  self.test_add_team:'Add Team',
                  self.test_add_attendee_to_team:'Add Attendee to Team',
                  self.test_add_sponsor:'Add Sponsor',
                  self.test_add_note:'Add Note',
                  self.test_add_note_to_sponsor:'Add Note to Sponsor' }

        results = { tests[f]:f() for f in tests }
        return results