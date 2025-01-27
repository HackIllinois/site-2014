from google.appengine.ext import ndb
import constants
from Model import Model
from Room import Room
from google.appengine.ext.db import BadValueError

class NewsFeedItem(Model):
	Model._automatically_add_event_as_ancestor()

	description = ndb.TextProperty()
	time = ndb.IntegerProperty()
	icon_url = ndb.TextProperty()
	highlighted = ndb.JsonProperty() #[[range,color],[range,color]],
	emergency = ndb.BooleanProperty()
	hackillinois = ndb.BooleanProperty(default=False)
	announcement = ndb.BooleanProperty(default=False)

	@classmethod
	def new(cls, data):
		skills = cls()
		for k in data:
			setattr(skills, k, data[k])
		return skills
