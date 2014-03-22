#!/usr/bin/python
import json
import urllib
import httplib2
from redis import Redis
from rq import Queue
import googledatastore as datastore
from googledatastore.helper import *
#from worker_functions import *

#METADATA_SERVER = 'http://metadata/computeMetadata/v1/instance/service-accounts'
#SERVICE_ACCOUNT = 'default'
#GOOGLE_STORAGE_PROJECT_NUMBER = '1024924889757'
#'x-goog-project-id': GOOGLE_STORAGE_PROJECT_NUMBER

#access_token = ''

"""This script grabs a token from the metadata server, and queries the
Google Cloud Storage API to list buckets for the desired project."""

def main():
  datastore.set_options(dataset='hackillinois')
  res = getData()
  print res

def getData():
  req = datastore.RunQueryRequest()
  q = req.query
  set_kind(q, kind='Task')
  set_composite_filter(q.filter,
                     datastore.CompositeFilter.AND,
                     set_property_filter(
                         datastore.Filter(),
                         'complete', datastore.PropertyFilter.EQUAL, False))
  resp = datastore.run_query(req)
  result = Set([])
  for r in resp.batch.entity_result:
    # key, jobFunction, data
    result.add([r.entity.key, r.entity.property[0].value.string_value,r.entity.property[1].value.boolean_value])
  return result


"""
def getToken():
  token_uri = '%s/%s/token' % (METADATA_SERVER, SERVICE_ACCOUNT)
  http = httplib2.Http()
  resp, content = http.request(token_uri, method='GET', body=None, headers={'X-Google-Metadata-Request': 'True'}) # Make request to metadata server

  if resp.status == 200:
    d = json.loads(content)
    access_token = d['access_token'] # Save the access token
    return True
  else:
    return False

def getData():
    # Construct the request to Google
    # Needs to be updated to the cloud datastore api
    query = "SELECT * FROM Task"
    http = httplib2.Http()
    resp, content = http.request('https://www.googleapis.com/datastore/v1beta2/datasets/hackillinois/runQuery', \
                                  method='POST', \
                                  body='{ "gqlQuery": {"queryString": "'+query+'","allowLiteral": true}}', \
                                  headers={'Authorization': 'Bearer ' + access_token})

    if resp.status == 200:
       print content
    else:
       print resp.status
"""

if __name__ == '__main__':
  main()


q = Queue(connection=Redis())

#Enqueue to the workers from the datastore here and then save the result back into the datastore
"""
example Enqueue
result = q.enqueue(count_words_at_url, 'http://google.com')
"""