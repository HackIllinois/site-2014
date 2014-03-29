import MainHandler
import cgi, urllib, logging, re, datetime

from db.Sponsor import Sponsor

from db.Attendee import Attendee
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from collections import defaultdict
from google.appengine.api import memcache

from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from StringIO import StringIO

import urllib2

def addResource(zfile, url, fname):
    # get the contents
    contents = urlfetch.fetch(url).content
    # write the contents to the zip file
    zfile.writestr(fname, contents)

class SponsorDownloadHandler(MainHandler.Handler, webapp.RequestHandler):
    def get(self):
        data = memcache.get('hackers')
        if not data:
            hackers = Attendee.search_database({'isRegistered':True})
            data = {}
            data['hackers'] = []
            for hacker in hackers:
                data['hackers'].append({ 'nameFirst':hacker.nameFirst,
                                         'nameLast':hacker.nameLast,
                                         'email':hacker.email,
                                         'gender':hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                                         'school':hacker.school,
                                         'year':hacker.year,
                                         'linkedin':hacker.linkedin,
                                         'github':hacker.github,
                                         'projectType':hacker.projectType,
                                         'resume':hacker.resume,
                                         'isApproved':hacker.isApproved,
                                         'userId':hacker.userId})

            if not memcache.set('hackers', data, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Hackers:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.render("sponsor_download.html", data=data)

    def post(self):
        download = self.request.get('download[]', allow_multiple=True)
        logging.info(len(download))
        for cur_download in download:
            logging.info(cur_download.split('-', 1)[0])
            logging.info(cur_download.split('-', 1)[1])