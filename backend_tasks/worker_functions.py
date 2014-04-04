import zipfile, os
import googledatastore as datastore
from googledatastore.helper import *

"""
All Task functions go here, to be executed from the queue and Rq workers
"""

#Base directory where all of the resume's are held (needs a trailing slash)
directoryBase = ''

def zip_resumes(data, key, obj):
    #copy resume files to a staging directory
    #zip that directory
    #serve it
    #update the database with the key
    stagingDir = directoryBase + 'staging/'+key.path_element.id[-1]
    os.makedirs(directory)
    for resume in data:
        copy(directoryBase+resume['gsObjectName']+'.pdf', stagingDir)
    toZip('serve/'+key.path_element.id[-1], stagingDir)

    #set the flag to complete
    obj.property[0].value.boolean_value = True
    req = datastore.CommitRequest()
    datastore.set_options(dataset='hackillinois')
    req.mode = datastore.CommitRequest.NON_TRANSACTIONAL
    req.mutation.update.extend([obj])
    datastore.commit(req)



#zips a full directory
def toZip(name, directory):
    zippedHelp = zipfile.ZipFile(name+".zip", "w", compression=zipfile.ZIP_DEFLATED )
    list = os.listdir(directory)
    
    for entity in list:
        each = os.path.join(directory,entity)
 
        if os.path.isfile(each):
            print each
            zippedHelp.write(each,zipfile.ZIP_DEFLATED)
        else:
            addFolderToZip(zippedHelp,entity)
    zippedHelp.close()