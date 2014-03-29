from google.appengine.ext import ndb
import constants
from Model import Model
from Room import Room
from google.appengine.ext.db import BadValueError

class Schedule(Model):
	Model._automatically_add_event_as_ancestor()

	event_name = StringProperty()
	description = TextProperty()
	location = StructuredProperty(Room)
	time = IntegerProperty()
	icon_url = TextProperty()

	@classmethod
	def new(cls, data):
		skills = cls()
		for k in data:
			setattr(skills, k, data[k])
		return skills

	@classmethod
	def unique_properties(cls):
		return ['event_name']