from google.appengine.ext import ndb
from Model import Model

class ApplyErrors(Model):
    # This is the workaround for the strong consistency
    Model._automatically_add_event_as_ancestor()



    @classmethod
    def new(cls, data):
        errors = cls()
        for k in data:
            setattr(errors, k, data[k])
        return errors
