from google.appengine.ext import ndb
import datetime as dt
import constants

### I probably broke all of this. :) --Matthew

'''
NDB cheatsheet: https://docs.google.com/document/d/1AefylbadN456_Z7BZOpZEXDq8cR8LYu7QgI7bt5V0Iw/edit#
NDB documentation: https://developers.google.com/appengine/docs/python/ndb/

To run all unit tests:

from pprint import pprint
from db import models
ut = models.UnitTest()
pprint(ut.run_all())

'''

class UnitTest(object):
    ''' To run all unit tests:
    from pprint import pprint
    from db import models
    ut = models.UnitTest()
    pprint(ut.run_all())
    '''
    import sys

    def test_add_attendee(self):
        passed = True
        data = {'nameFirst':'Alex', 'nameLast':'Burck', 'email':'burck1@illinois.edu', 'year':4}
        try:
            me = f_add(Attendee, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed


    def test_add_team(self):
        passed = True
        data = {'name':'Test'}
        try:
            t = f_add(Team, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_attendee_to_team(self):
        passed = True
        data = {'nameFirst':'Alex', 'nameLast':'Burck', 'email':'burck1@illinois.edu', 'year':4}
        me = f_add(Attendee, data)
        data = {'name':'Test'}
        t = f_add(Team, data)
        try:
            passed = t.addMember(me)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_sponsor(self):
        passed = True
        data = {'companyName':'Test Company', 'contactName':'Qwerty Uiop', 'email':'qwerty@company.com'}
        try:
            s = f_add(Sponsor, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_note(self):
        passed = True
        data = {'emailTo':'burck1@illinois.edu', 'emailFrom':'qwerty@company.com', 'dateTime':dt.datetime.now(), 'subject':'Test', 'text':'Test'}
        try:
            n = f_add(Note, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_add_note_to_sponsor(self):
        passed = True
        data = {'companyName':'Test Company', 'contactName':'Qwerty Uiop', 'email':'qwerty@company.com'}
        s = f_add(Sponsor, data)
        data = {'emailTo':'burck1@illinois.edu', 'emailFrom':'qwerty@company.com', 'dateTime':dt.datetime.now(), 'subject':'Test', 'text':'Test'}
        n = f_add(Note, data)
        try:
            passed = s.addNote(n)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def run_all(self):
        tests = { self.test_add_attendee:'Add Attendee',
                  self.test_add_team:'Add Team',
                  self.test_add_attendee_to_team:'Add Attendee to Team',
                  self.test_add_sponsor:'Add Sponsor',
                  self.test_add_note:'Add Note',
                  self.test_add_note_to_sponsor:'Add Note to Sponsor' }

        results = { tests[f]:f() for f in tests }
        return results


class UnitTest2(object):
    ''' To run all unit tests:
    from pprint import pprint
    from db import models
    ut = models.UnitTest2()
    pprint(ut.run_all())
    '''
    import sys

    def test_add_attendee(self):
        passed = True
        data = {'nameFirst':'Alex', 'nameLast':'Burck', 'email':'burck1@illinois.edu', 'year':4}
        try:
            me = add(Attendee, data)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_update_attendee(self):
        passed = True
        data = {'year':1}
        search = {'email':'burck1@illinois.edu'}
        try:
            me = update_search(Attendee, data, search)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def test_delete_attendee(self):
        passed = True
        search = {'email':'burck1@illinois.edu'}
        try:
            me = delete_search(Attendee, search)
        except:
            passed = False
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return passed

    def run_all(self):
        tests = { self.test_add_attendee:'Add Attendee',
                  self.test_update_attendee:'Update Attendee',
                  self.test_delete_attendee:'Delete Attendee'
                  }

        results = { tests[f]:f() for f in tests }
        return results
