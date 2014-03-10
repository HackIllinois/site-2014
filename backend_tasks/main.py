#!/usr/bin/python
import json
import urllib
import httplib2
from redis import Redis
from rq import Queue
from worker_functions import *

METADATA_SERVER = 'http://metadata/computeMetadata/v1/instance/service-accounts'
SERVICE_ACCOUNT = 'default'
GOOGLE_STORAGE_PROJECT_NUMBER = 'YOUR_GOOGLE_STORAGE_PROJECT_NUMBER'

access_token = ''

"""This script grabs a token from the metadata server, and queries the
Google Cloud Storage API to list buckets for the desired project."""

def main():
	if getToken()
		#getData()
	else
		echo "Token Error"


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
    resp, content = http.request('https://storage.googleapis.com', \
                                  body=None, \
                                  headers={'Authorization': 'OAuth ' + access_token, \
                                           'x-goog-api-version': '2', \
                                           'x-goog-project-id': GOOGLE_STORAGE_PROJECT_NUMBER })

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