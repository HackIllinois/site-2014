from google.appengine.ext import ndb
import constants
from Model import Model
from Room import Room
from google.appengine.ext.db import BadValueError

class NewsFeedItem(Model):
	Model._automatically_add_event_as_ancestor()

	description = StringProperty()
	time = IntegerProperty()
	icon_url = TextProperty()
	highlighted = JsonProperty() #[[range,color],[range,color]],
	emergency = BooleanProperty()


	@classmethod
	def new(cls, data):
		skills = cls()
		for k in data:
			setattr(skills, k, data[k])
		return skills

	@classmethod
	def unique_properties(cls):
		return ['description']