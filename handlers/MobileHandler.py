import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from google.appengine.api import users, memcache
import json

