from google.appengine.ext import ndb
import constants
from Model import Model
from google.appengine.ext.db import BadValueError

class Skills(Model):
	Model._automatically_add_event_as_ancestor()

	name = ndb.StringProperty()
	tags = ndb.JsonProperty()
	alias = ndb.JsonProperty()

	@classmethod
	def new(cls, data):
		skills = cls()
		for k in data:
			setattr(skills, k, data[k])
		return skills

	@classmethod
	def unique_properties(cls):
		return ['name']