from google.appengine.ext import ndb
from db.Model import Model
from db import constants
from db.Attendee import Attendee
from db.Admin import Admin
from db.Sponsor import Sponsor

class MobileUser(Model):
	Model._automatically_add_event_as_ancestor()

	googleUser = ndb.UserProperty()

	staffModel =  ndb.StructuredProperty(Admin)
	attendeeModel = ndb.StructuredProperty(Attendee)
	companyRepModel = ndb.StructuredProperty(Sponsor)