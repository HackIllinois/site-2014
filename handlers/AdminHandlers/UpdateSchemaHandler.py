from google.appengine.ext import deferred
from google.appengine.ext import ndb

import logging

from db.Attendee import Attendee
from db.Status import Status
import MainAdminHandler


BATCH_SIZE = 100

def UpdateSchema(cursor=None, num_updated=0):
    query = Attendee.query()
    count = query.count()
    data, next_curs, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)

    to_put = []
    for p in data:
        # Entities to update
        p.approvalStatus = Status()
        to_put.append(p)

    if to_put:
        ndb.put_multi(to_put)
        num_updated += len(to_put)
        logging.info('Put %d entities to Datastore for a total of %d/%d', len(to_put), num_updated, count)
        deferred.defer(UpdateSchema, cursor=next_curs, num_updated=num_updated)
    else:
        logging.info('UpdateSchema complete with %d updates!', num_updated)


class UpdateSchemaHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        deferred.defer(UpdateSchema)
        self.write('Schema migration successfully initiated.')
