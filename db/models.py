from google.appengine.ext import ndb
import datetime as dt

'''
NDB cheatsheet: https://docs.google.com/document/d/1AefylbadN456_Z7BZOpZEXDq8cR8LYu7QgI7bt5V0Iw/edit#
NDB documentation: https://developers.google.com/appengine/docs/python/ndb/

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

def f_add(cls, data, search = {}):
    '''
    Creates a model and adds it to the database
    WILL NOT override data if already there

    @param cls: the class model to use
    @param data: the data to add in the database
    @param search: properties to search the database
    @return: whether or not the data was added to the database

    ex: add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'standing':3})
    Returns True if "doe1@illinois.edu" is not already in the database and data is successfully added
    Returns False otherwise
    OR
    add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'standing':3}, {'email':'doe1@illinois.edu'})
    Same result
    '''
    o = cls.new(data)
    o.put()
    # TODO: add check if already in database
    return o

def add(cls, data, search = {}):
    '''
    Creates a model and adds it to the database
    WILL NOT override data if already there
    WILL NOT add data if similar data is already there, determined by "search" or model's unique_properties() attribute

    @param cls: the class model to use
    @param data: the data to add in the database
    @param search: properties to search the database
    @return: whether or not the data was added to the database

    ex: add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'standing':3})
    Returns True if "doe1@illinois.edu" is not already in the database and data is successfully added
    Returns False otherwise
    OR
    add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'standing':3}, {'email':'doe1@illinois.edu'})
    Same result
    '''
    if(search == {}):
        try:
            properties = cls.unique_properties()
            for p in properties:
                search[p] = data[p]
        except AttributeError:
            #class does not have attribute unique_properties()
            o = cls.new(data)
            o.put()
            return o
        except LookupError:
            #data does not key "p"
            return False
    if not in_database(cls, search):
        o = cls.new(data)
        o.put()
        return o
    return False

def delete_search(cls, search):
    '''
    deletes a model in the database

    @param cls: the class model to use
    @param search: the parameters to search with
    @return: nothing

    ex: update_model(Attendee, {'email':'doe1@illinois.edu', 'standing':3})
    '''
    #These functions need to be changed to delete all references a model ex. an Attendee in a Team
    m = search_database(cls, search).get()
    if m != None:
        delete(cls, m.key)

def delete(cls, key):
    '''
    deletes a model in the database

    @param cls: the class model to use
    @param key: key to delete
    @return: nothing

    ex: update_model(Attendee, key)
    '''
    #These functions need to be changed to delete all references a model ex. an Attendee in a Team
    key.delete()

def update_search(cls, data, search = {}):
    '''
    Updates a model in the database
    WILL override data if already there

    @param cls: the class model to use
    @param data: the data to change in the database
    @param search: the parameters to search with
    @return: whether or not the data was found in the database and updated

    ex: update_model(Attendee, {'nameFirst':'John', 'nameLast':'Doe'}, {'email':'doe1@illinois.edu', 'standing':3})
    '''
    if(search == {}):
        try:
            properties = cls.unique_properties()
            for p in properties:
                search[p] = data[p]
        except AttributeError:
            #class does not have attribute unique_properties()
            return False
        except LookupError:
            #data does not key "p"
            return False
    m = search_database(cls, search).get()
    if m != None:
        return update(cls, data, m.key)
    return False

def update(cls, data, key):
    '''
    Updates a model in the database
    WILL override data if already there

    @param cls: the class model to use
    @param data: the data to change in the database
    @param key: key of model
    @return: whether or not the data was updated

    ex: update_model(Attendee, {'nameFirst':'John', 'nameLast':'Doe'}, key)
    '''
    u = key.get()
    for p in data:
        setattr(u, p, data[p])
    u.put()
    return u

def add_or_update(cls, data, search = {}):
    '''
    Adds or updates a model in the database
    WILL override data if already there

    @param cls: the class model to use
    @param data: the data to change in the database
    @param search: the parameters to search with
    @return: nothing

    ex: update_model(Attendee, {'nameFirst':'John', 'nameLast':'Doe'}, {'email':'doe1@illinois.edu', 'standing':3})
    '''
    if not add(cls, data, search):
        update(cls, data, search)

def in_database(cls, search):
    '''
    Determines if the data already in the database, determined by "search"
    DOES NOT effect the database

    @param cls: the class model to use
    @param search: the data used to search the database
    @return: True if the data is in the database, False otherwise

    ex: in_database(Attendee, {'email':'doe1@illinois.edu'})
    Returns True if "doe1@illinois.edu" is already in the database
    Returns False otherwise
    '''
    return search_database(cls,search).get() != None

def search_database(cls, search, perfect_match=True):
    '''
    Searches the database for models matching "search"
    DOES NOT effect the database

    @param cls: the class model to use
    @param search: the data used to search the database
    @perfect_match:	True = every argument matches : False = one argument matches
    @return: iterator of models

    ex: search_database(Attendee, {'email':'doe1@illinois.edu'})
    '''
    if search == {}:
        return cls.gql()
    q = "WHERE "
    if perfect_match:
        ao = " AND "
    else:
	    ao = " OR "
    for param in search:
        q += param + " = '" + search[param] + "'" + ao
    return cls.gql(q[:-len(ao)])

class Attendee(ndb.Model):
    # For user object look at https://developers.google.com/appengine/docs/python/users/userclass
    userNickname = ndb.StringProperty()
    userEmail = ndb.StringProperty()
    userId = ndb.StringProperty()
    userFederatedIdentity = ndb.StringProperty()
    userFederatedProvider = ndb.StringProperty()

    nameFirst = ndb.StringProperty(required=True)
    nameLast = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    gender = ndb.StringProperty(choices=['Male','Female','NA'])
    school = ndb.StringProperty()
    standing = ndb.StringProperty(choices=['Freshman','Sophomore','Junior','Senior','Grad','Other'])

    experience = ndb.TextProperty() # unlimited length, not indexed
    resumePath = ndb.StringProperty()
    linkedin = ndb.StringProperty()
    github = ndb.StringProperty()

    shirt = ndb.StringProperty(choices=['XS','S','M','L','XL','XXL'])
    food = ndb.StringProperty(choices=['None','Vegetarian','Vegan','Gluten Free'])

    recruiters = ndb.BooleanProperty(default=False)
    picture = ndb.BooleanProperty(default=False)
    termsOfService = ndb.BooleanProperty(default=False)

    isAdmin = ndb.BooleanProperty(default=False)
    isParticipant = ndb.BooleanProperty(default=False)
    registrationTime = ndb.DateTimeProperty(auto_now_add=True)

    teamMembers = ndb.TextProperty()
    approved = ndb.StringProperty()

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
    def unique_properties(cls):
        return ['email']

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
    def unique_properties(cls):
        return ['name']

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
            me = f_add(Attendee, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed


    def test_add_team(self):
        passed = True
        data = {'name':'Test'}
        try:
            t = f_add(Team, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_attendee_to_team(self):
        passed = True
        data = {'nameFirst':'Alex', 'nameLast':'Burck', 'email':'burck1@illinois.edu', 'standing':4}
        me = f_add(Attendee, data)
        data = {'name':'Test'}
        t = f_add(Team, data)
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
            s = f_add(Sponsor, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_note(self):
        passed = True
        data = {'emailTo':'burck1@illinois.edu', 'emailFrom':'qwerty@company.com', 'dateTime':dt.datetime.now(), 'subject':'Test', 'text':'Test'}
        try:
            n = f_add(Note, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_note_to_sponsor(self):
        passed = True
        data = {'companyName':'Test Company', 'contactName':'Qwerty Uiop', 'email':'qwerty@company.com'}
        s = f_add(Sponsor, data)
        data = {'emailTo':'burck1@illinois.edu', 'emailFrom':'qwerty@company.com', 'dateTime':dt.datetime.now(), 'subject':'Test', 'text':'Test'}
        n = f_add(Note, data)
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


class UnitTest2(object):
    ''' To run all unit tests:
    from pprint import pprint
    from db import models
    ut = models.UnitTest2()
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

    def test_update_attendee(self):
        passed = True
        data = {'standing':1}
        search = {'email':'burck1@illinois.edu'}
        try:
            me = update_search(Attendee, data, search)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_delete_attendee(self):
        passed = True
        search = {'email':'burck1@illinois.edu'}
        try:
            me = delete_search(Attendee, search)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def run_all(self):
        tests = { self.test_add_attendee:'Add Attendee',
                  self.test_update_attendee:'Update Attendee',
                  self.test_delete_attendee:'Delete Attendee'
                  }

        results = { tests[f]:f() for f in tests }
        return results