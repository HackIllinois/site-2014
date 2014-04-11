from google.appengine.ext import deferred
from google.appengine.ext import ndb

import logging

from db.Attendee import Attendee
from db.Sponsor import Sponsor
from db.Admin import Admin
from db.Status import Status
from db import constants
import MainAdminHandler


BATCH_SIZE = 100

def UpdateSchema(cursor=None, count=0):
    query = Attendee.query()
    count += query.count()
    data, next_curs, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)

    to_put = []
    for p in data:
        if not p.approvalStatus:
            p.approvalStatus = Status()
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
