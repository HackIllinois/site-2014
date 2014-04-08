import zipfile, os, json, time
import googledatastore as datastore
import shutil
from googledatastore.helper import *

"""
All Task functions go here, to be executed from the queue and Rq workers
"""

#Base directory where all of the resume's are held (needs a trailing slash)
directoryBase = '/home/Austin/hackillinois-website/backend_tasks/'

#copy resume files to a staging directory
#zip that directory
#serve it
#update the database with the key
def zip_resumes(data, key, obj):
    errors = []
    stagingDir = '%sstaging/%s' % (directoryBase, key.path_element[-1].id)
    print 'Staging directory: %s' % stagingDir
    if os.path.isdir(stagingDir):
        shutil.rmtree(stagingDir)
    os.makedirs(stagingDir)
    for resume in data:
        tempLoc = '%sfiles/%s.pdf' % (directoryBase, resume['gsObjectName'])
        print "Staging: %s" % (resume['gsObjectName'])
        if os.path.isfile(tempLoc):
            shutil.copy(tempLoc, stagingDir+'/'+resume['fileName']+'.pdf')
            print " - %s.pdf" % resume['fileName']
        else:
            errors.append("No resume %s(%s)." % (resume['fileName'],resume['gsObjectName']))
    serveLoc = "%s/serve" % (directoryBase)
    if toZip(stagingDir, stagingDir, serveLoc):
        #set the flag to complete
        for thing in obj.property:
            lookup = thing.name
            if lookup == "complete":
                thing.value.boolean_value = True
            elif lookup == "completeTime":
                thing.value.timestamp_microseconds_value  = long(time.time() * 1000000.0)
            elif lookup == "errorMessages":
                thing.value.string_value = json.dumps(errors)
        req = datastore.CommitRequest()
        datastore.set_options(dataset='hackillinois')
        req.mode = datastore.CommitRequest.NON_TRANSACTIONAL
        req.mutation.update.extend([obj])
        datastore.commit(req)

#zips a full directory
def toZip(name, initialDir, finalDir):
    try:
        print "Starting zipping."
        zipIt = zipfile.ZipFile(name+".zip", "w", compression=zipfile.ZIP_DEFLATED)
        listdir = os.listdir(initialDir)
        for entity in listdir:
            each = os.path.join(initialDir,entity)
            if os.path.isfile(each):
                (head, tail) = os.path.split(each)
                zipIt.write(each,tail)
        zipIt.close()
        print "Moving to serve."
        shutil.move(name+".zip", finalDir)
        (head, tail) = os.path.split(finalDir)
        print "Serving @ http://23.236.61.209/serve/%s.zip" % (name)
        return True
    except:
        return False