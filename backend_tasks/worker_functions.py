import zipfile, os, json
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
    stagingDir = '%sstaging/%s' % (directoryBase, key.path_element[-1].id)
    print 'Staging: %s' % stagingDir
    os.makedirs(stagingDir)
    data = json.loads(data)
    for resume in data:
        tempLoc = '%sfiles/%s.pdf' % (directoryBase, resume['gsObjectName'])
        print tempLoc
        shutil.copy(tempLoc, stagingDir)
    serve = '%s/serve' % directoryBase
    if toZip(stagingDir, stagingDir, serve):
        #set the flag to complete
        obj.property[0].value.boolean_value = True
        req = datastore.CommitRequest()
        datastore.set_options(dataset='hackillinois')
        req.mode = datastore.CommitRequest.NON_TRANSACTIONAL
        req.mutation.update.extend([obj])
        datastore.commit(req)



#zips a full directory
def toZip(name, initialDir, finalDir):
    try:
        zipIt = zipfile.ZipFile(name+".zip", "w", compression=zipfile.ZIP_DEFLATED)
        listdir = os.listdir(initialDir)
        for entity in listdir:
            each = os.path.join(initialDir,entity)
            if os.path.isfile(each):
                (head, tail) = os.path.split(each)
                zipIt.write(each,tail)
        zipIt.close()
        shutil.move(name+".zip", finalDir)
        return True
    except:
        return False