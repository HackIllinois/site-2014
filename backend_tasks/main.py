#!/usr/bin/python
import boto
from gslib.third_party.oauth2_plugin import oauth2_plugin
from gslib.third_party.oauth2_plugin import oauth2_client
import multiprocessing, threading, time
import os, sys
import json
import urllib, httplib2
from redis import Redis
from rq import Queue, Connection, Worker
import googledatastore as datastore
from googledatastore.helper import *
from worker_functions import *

NUM_WORKERS = 1
BASE_LOC = '/home/Austin/hackillinois-website/backend_tasks/'
# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'
BUCKET = 'hackillinois'
RDq = Queue(connection=Redis())
workers = []

try:
  oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
except:
  oauth2_client.token_exchange_lock = threading.Lock()

def manageWorkers(cmd):
  with Connection():
    if cmd == "start":
      for x in range(0,NUM_WORKERS):
        w = Worker([Queue()])
        w.work()
        workers.append(w)
    elif cmd == "stop":
      if len(workers) > 0:
        for worker in workers:
          os.kill(worker.pid, signal.SIGINT)
        workers = []
  

def setup():
  try:
    oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
  except:
    oauth2_client.token_exchange_lock = threading.Lock()
  datastore.set_options(dataset='hackillinois')

def getTasks():
    print "Zipping resumes: "
    setup()
    data = getData()
    if len(data) != 0:
      for item in data:
        enqueue(data)
    else:
      print "No jobs!"

def main():
  if len(sys.argv) > 1:
    if sys.argv[1] == "refresh":
      print "Stopping workers and downloading resumes: "
      manageWorkers("stop")
      if downloadAllResumes():
        print "Getting tasks: "
        getTasks()
        manageWorkers("start")
    elif sys.argv[1] == "download":
      print "Downloading resumes: "
      downloadAllResumes()
    elif sys.argv[1] == "help":
      print "Run refresh to download resumes and start to queue up tasks and start up the workers.\nCommands: \nstart\nstop\nrefresh\ndownload\ntasks"
    elif sys.argv[1] == "tasks":
      print "Getting tasks: "
      getTasks()
    elif sys.argv[1] == "start":
      getTasks()
      manageWorkers("start")
    elif sys.argv[1] == "stop":
      manageWorkers("stop")
  else:
    print "You need a command, use help for more information."

def getData():
  req = datastore.RunQueryRequest()
  gql_query = req.gql_query
  gql_query.query_string = 'SELECT * FROM Task WHERE complete = FALSE'
  gql_query.allow_literal = True
  resp = datastore.run_query(req)
  print "%s new incomplete requests found." % len(resp.batch.entity_result)
  result = []
  for r in resp.batch.entity_result:
    data = []
    func = ''
    for thing in r.entity.property:
      lookup = thing.name
      if lookup == "data":
        data = json.loads(thing.value.string_value)
      elif lookup == "jobFunction"
        func = thing.value.string_value
    result.append([r.entity.key, func, data, r.entity])
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
  if os.path.isdir(filesLoc) == False:
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
  return True

if __name__ == '__main__':
  main()