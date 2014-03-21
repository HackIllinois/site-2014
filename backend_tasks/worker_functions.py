import requests
import zipfile, os

"""
All Task functions go here, to be executed from the queue and Rq workers
"""

#remove, not needed, just a placeholder
def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

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