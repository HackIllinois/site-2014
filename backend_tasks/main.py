#!/usr/bin/python
import json
import urllib
import httplib2
from redis import Redis
from rq import Queue
#from worker_functions import *

METADATA_SERVER = 'http://metadata/computeMetadata/v1/instance/service-accounts'
SERVICE_ACCOUNT = 'default'
GOOGLE_STORAGE_PROJECT_NUMBER = '1024924889757'
#'x-goog-project-id': GOOGLE_STORAGE_PROJECT_NUMBER

access_token = ''

"""This script grabs a token from the metadata server, and queries the
Google Cloud Storage API to list buckets for the desired project."""

def main():
	if getToken():
		getData()
	else:
		print "Token Error"


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
                                  headers={'Authorization': 'OAuth ' + access_token})

    if resp.status == 200:
       print content
    else:
       print resp.status

if __name__ == '__main__':
  main()


q = Queue(connection=Redis())

#Enqueue to the workers from the datastore here and then save the result back into the datastore
"""
example Enqueue
result = q.enqueue(count_words_at_url, 'http://google.com')
"""