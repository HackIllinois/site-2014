import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from db.mobile import MobileConstants
from db.mobile.Staff import Staff
from db.mobile.CompanyRep import CompanyRep
from db.mobile.Hacker import Hacker
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
        return self.write(json.dumps(MobileConstants.ROOM))

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
        return self.write(json.dumps(MobileConstants.SUPPORT_TYPE))

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
        if 'AuthName' in self.request.headers and self.request.headers['AuthName'] != 'test':
            staffProfiles = Staff.search_database({})
            listOfStaff = []
            for staffProfile in staffProfiles:
                _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase}

        elif self.request.headers['AuthName'] == 'test':
            return self.write(json.dumps([{'name':'Jacob', 'email':'cool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'room #4', 'skills':'awesome'}, {'name':'Alex', 'email':'Alexcool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'1109', 'skills':'awesome'}]))

        else:
            return self.write(json.dumps({'access':'No Access'}))    


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
        if 'AuthName' in self.request.headers and self.request.headers['AuthName'] != 'test':
            hackerProfiles = Hacker.search_database({})
            listOfHackers = []
            for hackerProfile in hackerProfiles:
                _hacker = {'name':hackerProfile.name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase}
                listOfHackers.append(_hacker)
            return self.write(json.dumps(listOfHackers))

        elif self.request.headers['AuthName'] == 'test':
            return self.write(json.dumps([{'name':'Jacob', 'email':'cool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'room #4', 'skills':'awesome'}, {'name':'Alex', 'email':'Alexcool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'1109', 'skills':'awesome'}]))

        else:
            return self.write(json.dumps({'access':'No Access'}))    


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
        if 'AuthName' in self.request.headers and self.request.headers['AuthName'] != 'test':
            hackerProfile = Hacker.search_database({'userId':self.request.headers['AuthName']}).get()
            _hacker = {'name':hackerProfile.name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase}
            return self.write(json.dumps(_hacker))

        elif self.request.headers['AuthName'] == 'test':
            return self.write(json.dumps({'name':'Jacob', 'email':'email@gmail.com', 'school':'uiuc', 'year':'senior', 'skills':'none', 'homebase':'1105'}))

        else:
            return self.write(json.dumps({'access':'No Access'}))

    def Post(self):
        if 'AuthName' in self.request.headers and self.request.headers['AuthName'] != 'test':
            updatedHackerProfile = self.request.POST.items()
            updatedHackerProfileDict = {}
            for _key,_value in updatedHackerProfile:
                updatedHackerProfileDict[_key] = _value

            Hacker.update_search(params, updatedHackerProfileDict)

'''
        for example:
            [
                company name: {
                    name: ,
                    company: ,
                    job title: ,
                    skills: ,
                    events: ,
                    email/contact: ,
                }
            ]

    Note:
'''
class CompaniesHandler(MainHandler.BaseMobileHandler):

    '''

        @return The models of all the Companies attending HackIllinois
    '''
    def get(self):
        if 'AuthName' in self.request.headers and self.request.headers['AuthName'] != 'test':
            companyProfiles = {}

            for companyName in MobileConstants.COMPANY_NAMES:
                companyProfiles[companyName] = []
                companyProfile = CompanyRep.search_database({'company':companyName})
                for _companyRep in companyProfile:
                    companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'jobTitle':_companyRep.jobTitle, 'skills':_companyRep.skills}
                    _list = companyProfiles[companyName]
                    _list.append(companyRepProfile)
            return self.write(json.dumps(companyProfiles))

        elif self.request.headers['AuthName'] == 'test':
            companyProfiles = {}

            for companyName in MobileConstants.COMPANY_NAMES:
                companyProfiles[companyName] = []
                companyProfile = CompanyRep.search_database({'company':companyName})
                for _companyRep in companyProfile:
                    companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'jobTitle':_companyRep.jobTitle, 'skills':_companyRep.skills}
                    companyProfiles[companyName].append(companyRepProfile)
            return self.write(json.dumps(companyProfiles))

        else:
            return self.write(json.dumps({'access':'No Access'}))

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
        return self.write(json.dumps(MobileConstants.SKILLS))

    # def put(self):
    #     pass
