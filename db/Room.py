from google.appengine.ext import ndb
import constants
from Model import Model
from google.appengine.ext.db import BadValueError

class Room(Model):
	Model._automatically_add_event_as_ancestor()

	building = StringProperty()
	floor = IntegerProperty()
	number = IntegerProperty()
	room_type = StringProperty()
	name = StringProperty()
	image_url = TextProperty()

	@classmethod
	def new(cls, data):
		skills = cls()
		for k in data:
			setattr(skills, k, data[k])
		return skills

	@classmethod
	def unique_properties(cls):
		return ['name']