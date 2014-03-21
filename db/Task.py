from Model import Model
from google.appengine.ext import ndb

class Task(Model):
    # This is the workaround for the strong consistency
    Model._automatically_add_event_as_ancestor()

    jobFunction = ndb.StringProperty(required=True)
    complete = ndb.BooleanProperty(default=False)
    data = ndb.JsonProperty(default='[]')
    creationTime = ndb.DateTimeProperty()
    errorMessages = ndb.TextProperty()

    @classmethod
    def new(cls, data):
        task = cls()
        for k in data:
            setattr(task, k, data[k])
        return task