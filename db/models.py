from google.appengine.ext import db

class Attendee(db.Model):
	name = db.StringProperty(required=True)
	isAdmin = db.BooleanProperty()//Set Default to False
	isParticipant = db.BooleanProperty()//Set Default to False
	email = db.EmailProperty()
	standing = db.IntegerProperty()
	teamID = db.IntegerProperty()