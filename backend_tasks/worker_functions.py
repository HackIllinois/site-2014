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
    print 'Staging: %s' % stagingDir
    if os.path.isdir(stagingDir):
        shutil.rmtree(stagingDir)
    os.makedirs(stagingDir)
    try:
        data = json.loads(data)
    except:
        data = []
    for resume in data:
        tempLoc = '%sfiles/%s.pdf' % (directoryBase, resume['gsObjectName'])
        print " - %s.pdf" % resume['gsObjectName']
        if os.path.isfile(tempLoc):
            shutil.copy(tempLoc, stagingDir)
        else:
            errors.append('No resume for %s.'resume['gsObjectName'])
    serve = '%s/serve' % directoryBase
    if toZip(stagingDir, stagingDir, serve):
        #set the flag to complete
        obj.property[0].value.boolean_value = True
        obj.property[2].value.timestamp_microseconds_value  = long(time.time() * 1000000.0)
        obj.property[4].value.string_value = json.dumps(errors)
        req = datastore.CommitRequest()
        datastore.set_options(dataset='hackillinois')
        req.mode = datastore.CommitRequest.NON_TRANSACTIONAL
        req.mutation.update.extend([obj])
        datastore.commit(req)



#zips a full directory
def toZip(name, initialDir, finalDir):
    try:
        print "Zipping."
        zipIt = zipfile.ZipFile(name+".zip", "w", compression=zipfile.ZIP_DEFLATED)
        listdir = os.listdir(initialDir)
        for entity in listdir:
            each = os.path.join(initialDir,entity)
            if os.path.isfile(each):
                (head, tail) = os.path.split(each)
                zipIt.write(each,tail)
        zipIt.close()
        shutil.move(name+".zip", finalDir)
        (head, tail) = os.path.split(finalDir)
        print "Serving %s." % tail
        return True
    except:
        return False