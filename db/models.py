from google.appengine.ext import db

''' Test Script
from db import db
from db import models
import datetime as dt

a = models.Attendee.new('Alex Burck', 'burck1@illinois.edu', 3)
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

class Attendee(db.Model):
    name = db.StringProperty(required=True)
    isAdmin = db.BooleanProperty(default=False) #Set Default to False
    isParticipant = db.BooleanProperty(default=True) #Set Default to False
    email = db.EmailProperty(required=True)
    standing = db.IntegerProperty() # 0=fresh, 1=soph, 2=jr, 3=sr, 4=grad
    registrationTime = db.DateTimeProperty(auto_now_add=True)
    team = db.Key()

    @classmethod
    def new(cls, mName, mEmail, mStanding):
        return cls(name=mName, email=mEmail, standing=mStanding)


class Team(db.Model):
    name = db.StringProperty(required=True)
    teamMembers = db.ListProperty(type(db.Key()))

    @classmethod
    def new(cls, mName):
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
    def new(cls, mEmailTo, mEmailFrom, mDateTime, mSubject, mText):
        return cls(emailTo=mEmailTo, emailFrom=mEmailFrom, dateTime=mDateTime, subject=mSubject, text=mText)

class Sponsor(db.Model):
    companyName = db.StringProperty(required=True)
    contactName = db.StringProperty()
    email = db.EmailProperty(required=True)
    levelOfSponsorship = db.IntegerProperty()
    notes = db.ListProperty(type(db.Key()))

    @classmethod
    def new(cls, mCompanyName, mContactName, mEmail):
        return cls(companyName=mCompanyName, contactName=mContactName, email=mEmail)

    def addNote(self, note):
        if type(note) == Note:
            self.notes.append(note.key())
        return type(note) == Note