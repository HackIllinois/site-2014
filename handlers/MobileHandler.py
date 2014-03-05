import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from google.appengine.api import users, memcache
import json

'''

    for example:
        [
            {
                event name: ,
                description: ,
                location: ,
                time: ,

            }
        ]

    Note:
'''
class ScheduleHandler(MainHandler.BaseMobileHandler):

    '''
        Get the current schedule of HackIllinois
            for example:

        @return the schedule of HackIllinois
    '''
    def get(self):
        return self.write(json.dumps([{'event name':'First Event' ,'description':'Blast Off' ,'location':'room #1' ,'time':'12:00pm'}]))

'''

    Note:
'''
class MapsHandler(MainHandler.BaseMobileHandler):

    '''

        @return A dictionary of each location and the value is a dictionary of floors and a list of rooms on each floor
            for example:
                {
                    "Siebel":{
                        "1":["Ground Zero", "Space Station"]
                    },
                    "DCL":{
                        "1":["Galaxy"]
                    }
                }
    '''
    def get(self):
        return self.write(json.dumps({'Siebel':{'1':['Ground Zero', 'Space Station']},'DCL':{'1':['Galaxy']}}))

'''


    Note:
'''
class SupportTypeHandler(MainHandler.BaseMobileHandler):

    '''

        @return The list of Support Types
            for example:
                {
                    "General":[events schedule, rules, comments/suggestions],
                    "Requests":[food & drinks, medical, equipment, other],
                    "Technical":[WIFI, power, locked out, other]
                }
    '''
    def get(self):
        return self.write(json.dumps({'General':['events schedule', 'rules', 'comments/suggestions'],'Requests':['food & drinks', 'medical', 'equipment', 'other'],"Technical":['WIFI', 'power', 'locked out', 'other']}))

'''

    for example:
        [
            {
                announcement:
            }
        ]

    Note:
'''
class EmergencyHandler(MainHandler.BaseMobileHandler):

    '''


        @return Emergency Messages
    '''
    def get(self):
        return self.write(json.dumps([{'announcement':'first emergency announcement of HackIllinois'}]))

    '''
        Update an Emergency Message

        @return Success or Fail (for now)
    '''
    def put(self):
        pass

'''

    for example:
        [
            {
                event name: ,
                location: ,
                time:
            }
        ]

    Note:
'''
class NewsfeedHandler(MainHandler.BaseMobileHandler):

    '''

        @parameter before Top bound on the time for the NewsFeed
        @parameter since Bottom bound on the time for the NewsFeed (default should be your last time of the NewFeed card you have)
        @return The NewFeed models that are between the before and since parameters
    '''
    def get(self):
        return self.write(json.dumps([{'event name':'first event of HackIllinois' ,'location':'room #1' ,'time':'1:00pm'}]))

    '''
        Add an item to the news feed. Only Admin/Staff will be able to use this functionality.

        @return Success or fail (for now)
    '''
#    def put(self):
#        pass

'''

    Note:
'''
class StaffHandler(MainHandler.BaseMobileHandler):

    '''

        for example:
            [
                {
                    name: ,
                    email: ,
                    school: ,
                    year: ,
                    homebase: ,
                    skills: ,
                }
            ]

        @return The models of all the Staff for HackIllinois
    '''
    def get(self):
        return self.write(json.dumps({'name':'Jacob', 'email':'cool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'room #4', 'skills':'awesome'}))

'''
        for example:
            [
                {
                    name: ,
                    email: ,
                    school: ,
                    year: ,
                    skills: ,
                    homebase: ,
                }
            ]

    Note:
'''
class HackersHandler(MainHandler.BaseMobileHandler):

    '''

        @return The models of all the Hackers attendeeing HackIllinois
    '''
    def get(self):
        return self.write(json.dumps([{'name':'Jacob', 'email':'cool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'room #4', 'skills':'awesome'}]))

'''
        for example:
            {
                name: ,
                email: ,
                school: ,
                year: ,
                skills: ,
                homebase: ,
            }

'''
class HackerHandler(MainHandler.BaseMobileHandler):

    def get(self):
        return self.write(json.dumps({'name':'Jacob', 'email':'cool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'room #4', 'skills':'awesome'}))

    def Post(self):
        pass

'''
        for example:
            [
                company name: {
                    name: ,
                    company: ,
                    job title: ,
                    skills: ,
                    events: ,
                    office hours: ,
                    email/contact: ,
                }
            ]

    Note:
'''
class CompaniesHandler(MainHandler.BaseMobileHandler):

    '''

        @return The models of all the Companies attendeeing HackIllinois
    '''
    def get(self):
        return self.write(json.dumps(
            {'Apple':
                {'name':'Joe Smith',
                 'company':'Apple',
                 'job title':'iOS Developer',
                 'skills':'cool things',
                 'events':'other cool things',
                 'office hours':'1:00 pm',
                 'email/contact':'coolemail@apple.com'}}))

'''

    for example:
        [
            skill1,
            skill2,
            skill3,
        ]

    Note:
'''
class SkillsHandler(MainHandler.BaseMobileHandler):

    '''

        @return A list of Skills that Hackers can have
    '''
    def get(self):
        return self.write(json.dumps(['skill1','skill2','skill3','skill4','skill5']))

    def put(self):
        pass
