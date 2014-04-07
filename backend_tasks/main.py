#!/usr/bin/python
import boto
from gslib.third_party.oauth2_plugin import oauth2_plugin
from gslib.third_party.oauth2_plugin import oauth2_client
import multiprocessing, threading, time
import os, sys
import json
import urllib, httplib2
from redis import Redis
from rq import Queue
import googledatastore as datastore
from googledatastore.helper import *
from worker_functions import *

BASE_LOC = '/home/Austin/hackillinois-website/backend_tasks/'
# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'
BUCKET = 'hackillinois'
RDq = Queue(connection=Redis())

try:
  oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
except:
  oauth2_client.token_exchange_lock = threading.Lock()


def setup():
  try:
    oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
  except:
    oauth2_client.token_exchange_lock = threading.Lock()
  datastore.set_options(dataset='hackillinois')

def main():
  if len(sys.argv) > 1:
    if sys.argv[1] == "refresh":
      print "Downloading resumes: "
      downloadAllResumes()
  else:
    print "Zipping resumes: "
    setup()
    data = getData()
    if len(data) != 0:
      for item in data:
        enqueue(data)
    else:
      print "No jobs!"

def getData():
  req = datastore.RunQueryRequest()
  gql_query = req.gql_query
  gql_query.query_string = 'SELECT * FROM Task WHERE complete = FALSE'
  gql_query.allow_literal = True
  resp = datastore.run_query(req)
  print "%s new incomplete requests found." % len(resp.batch.entity_result)
  result = []
  for r in resp.batch.entity_result:
    try:
      data = json.loads(r.entity.property[4].value.string_value)
    except:
      data = ''
    result.append([r.entity.key, r.entity.property[3].value.string_value,data,r.entity])
  return result

#Enqueue to the workers from the datastore here and then save the result back into the datastore
def enqueue(tasks):
  for task in tasks:
    RDq.enqueue_call(func='worker_functions.'+task[1],
               args=(task[2],task[0],task[3]),
               timeout=30)
  print "Enqueue done."

def downloadAllResumes():
  filesLoc = BASE_LOC+'files/'
  if !os.path.isdir(filesLoc):
      os.makedirs(filesLoc)
      os.makedirs(BASE_LOC+'serve/')
      os.makedirs(BASE_LOC+'staging/')
  uri = boto.storage_uri(BUCKET, GOOGLE_STORAGE)
  count = 0
  total = 0
  for obj in uri.get_bucket():
    if obj.size > 0:
      total += 1
  for obj in uri.get_bucket():
    if obj.size > 0:
      filename = filesLoc+obj.name+'.pdf'
      if os.path.isfile(filename):
        os.remove(filename)
      f = open(filename, 'w')
      count +=1
      print 'Downloading: %s of %s (%s %%), %sB' % (count, total, round(count/float(total)*100,2), obj.size)
      obj.get_contents_to_file(f)
      f.close()


if __name__ == '__main__':
  main()