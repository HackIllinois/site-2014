from google.appengine.ext import ndb
from Model import Model

class SignUp(Model):
    """ Emails collected before launching the full site """
    email = ndb.StringProperty(required=True)
    register_date = ndb.DateProperty()
