from google.appengine.ext import ndb
import constants
from Model import Model

class Status(Model):
    Model._automatically_add_event_as_ancestor()

    status = ndb.StringProperty(choices=constants.SHIRTS + [''], default='')

    @classmethod
    def new(cls, data):
        model = cls()
        for k in data:
            setattr(model, k, data[k])
        return model
