from google.appengine.ext import db

'''
How to add a Attendee to the datastore:

from db import db
from db import models
import datetime
a = models.Attendee(name='Alex Burck', isAdmin=True, isParticipant=False, email='burck1@illinois.edu')
a.standing = 3 # or you can set the parameters afterwords
a.teamID = 487
a.registrationTime = datetime.datetime.now()
a.put() # don't forget this
'''
class Attendee(db.Model):
	name = db.StringProperty(required=True)
	isAdmin = db.BooleanProperty() #Set Default to False
	isParticipant = db.BooleanProperty() #Set Default to False
	email = db.EmailProperty()
	standing = db.IntegerProperty() # 0=fresh, 1=soph, 2=jr, 3=sr, 4=grad
	teamID = db.IntegerProperty()
    registrationTime = db.DateTimeProperty()