from google.appengine.ext import deferred
from google.appengine.ext import ndb

import logging

from db.Attendee import Attendee
from db.Attendee import Attendee
from db.Attendee import Attendee
from db.Status import Status
from db import constants
import MainAdminHandler


BATCH_SIZE = 100

def UpdateSchema(cursor=None, count=0):
    query = Attendee.query()
    # query = Sponsor.query()
    # query = Admin.query()
    data, next_curs, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)

    to_put = []
    for p in data:
        # Entities to update
        p.database_key = constants.ATTENDEE_START_COUNT + count
        # p.database_key = constants.SPONSOR_START_COUNT + count
        # p.database_key = constants.ADMIN_START_COUNT + count
        to_put.append(p)
        count += 1

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
