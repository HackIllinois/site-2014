from google.appengine.ext import deferred
from google.appengine.ext import ndb

import logging
import random

from db.Attendee import Attendee
from db.Sponsor import Sponsor
from db.Admin import Admin
from db.Status import Status
from db import constants
import MainAdminHandler


BATCH_SIZE = 100

def get_next_key():
    key = None
    while not key:
        i = random.randint(constants.SPONSOR_START_COUNT, constants.SPONSOR_START_COUNT+9998)
        c = Sponsor.query(Sponsor.database_key == i).count()
        if c == 0: key = i
    return key

def UpdateSchema(cursor=None, count=0):
    query = Sponsor.query()
    count += query.count()
    data, next_curs, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)

    to_put = []
    for p in data:
        if not p.database_key:
            p.database_key = get_next_key()
        to_put.append(p)

    if to_put:
        ndb.put_multi(to_put)
        logging.info('Put %d entities to Datastore for a total of %d', len(to_put), count)
        deferred.defer(UpdateSchema, cursor=next_curs, count=count)
    else:
        logging.info('UpdateSchema complete with %d updates!', count)


class UpdateSchemaHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        deferred.defer(UpdateSchema)
        self.write('Schema migration successfully initiated.')
