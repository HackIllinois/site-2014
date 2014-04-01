#!/usr/bin/python
import json
import urllib
import httplib2
import os
import wget
from redis import Redis
from rq import Queue
import googledatastore as datastore
from googledatastore.helper import *
#from worker_functions import *

METADATA_SERVER = 'http://metadata/computeMetadata/v1/instance/service-accounts'
SERVICE_ACCOUNT = 'default'
GOOGLE_STORAGE_PROJECT_NUMBER = '1024924889757'
access_token = ''
# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'
BUCKET = 'hackillinois'
RDq = ''

def main():
  RDq = Queue(connection=Redis())
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
  result = []
  for r in resp.batch.entity_result:
    # key, jobFunction, data
    result.append([r.entity.key, r.entity.property[3].value.string_value,json.loads(r.entity.property[4].value.string_value)])
  return result

#Enqueue to the workers from the datastore here and then save the result back into the datastore
def enqueue(tasks):
  for task in tasks:
    RDq.enqueue_call(func=task[1],
               args=(task[2],task[0]),
               timeout=30)

def downloadAllResumes():
  if getToken():"""
    uri = boto.storage_uri(BUCKET, GOOGLE_STORAGE)
    dest_dir = '/var/hackillinois/'
    for filename in uri.get_bucket():
      src_uri = boto.storage_uri(BUCKET + '/' + filename, GOOGLE_STORAGE)

    # Create a file-like object for holding the object contents.
    object_contents = StringIO.StringIO()

    # The unintuitively-named get_file() doesn't return the object
    # contents; instead, it actually writes the contents to
    # object_contents.
    src_uri.get_key().get_file(object_contents)

    local_dst_uri = boto.storage_uri(
        os.path.join(dest_dir, filename), LOCAL_FILE)

    for dst_uri in (local_dst_uri, bucket_dst_uri):
      object_contents.seek(0)
      dst_uri.new_key().set_contents_from_file(object_contents)
    object_contents.close()"""


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
    http = httplib2.Http()
    resp, content = http.request('https://www.googleapis.com/storage/v1beta2/b/hackillinois/o', \
                                  body=None, \
                                  headers={'Authorization': 'OAuth ' + access_token, \
                                           'x-goog-api-version': '2', \
                                           'x-goog-project-id': GOOGLE_STORAGE_PROJECT_NUMBER })
    if resp.status == 200:
      jsonContent = json.loads(content)
      for item in jsonContent["items"]:
        if item["size"] > 0:
          #wget with item["mediaLink"]
          wget.download(item["mediaLink"])
    else:
       print resp.status


if __name__ == '__main__':
  main()