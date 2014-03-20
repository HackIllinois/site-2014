import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from db.mobile import MobileConstants
from db.Sponsor import Sponsor
from db.Admin import Admin
from google.appengine.api import users, memcache
import json


class ScheduleHandler(MainHandler.BaseMobileHandler):

    def get(self):
        return self.write(json.dumps([{'event name':'First Event' ,'description':'Blast Off' ,'location':'room #1' ,'time':'12:00pm'}]))


class MapsHandler(MainHandler.BaseMobileHandler):

    def get(self):
        return self.write(json.dumps(MobileConstants.ROOM))


class SupportTypeHandler(MainHandler.BaseMobileHandler):

    def get(self):
        return self.write(json.dumps(MobileConstants.SUPPORT_TYPE))


class EmergencyHandler(MainHandler.BaseMobileHandler):

    def get(self):
        return self.write(json.dumps([{'announcement':'first emergency announcement of HackIllinois'}]))

    def put(self):
        pass


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
   def put(self):
       pass

class StaffHandler(MainHandler.BaseMobileHandler):

    def get(self):
        if self.request.headers['AuthName'] == 'test':
            return self.write(json.dumps([{'name':'Jacob', 'email':'cool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'room #4', 'skills':'awesome', 'pictureURL':'url.com', 'status':'available'}, {'name':'Alex', 'email':'Alexcool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'1109', 'skills':'awesome', 'pictureURL':'url.com', 'status':'available'}]))

        elif 'AuthName' in self.request.headers:
            staffProfiles = Staff.search_database({})
            listOfStaff = []
            for staffProfile in staffProfiles:
                _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'pictureURL':staffProfile.pictureURL, 'status':staffProfile.status}

        else:
            return self.write()    


class HackersHandler(MainHandler.BaseMobileHandler):

    def get(self):
        if self.request.headers['AuthName'] == 'test':
            return self.write(json.dumps([{'name':'Jacob', 'email':'cool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'room #4', 'skills':'awesome', 'pictureURL':'url.com', 'status':'available'}, {'name':'Alex', 'email':'Alexcool@email.com', 'school':'U of I', 'year':'senior', 'homebase':'1109', 'skills':'awesome', 'pictureURL':'url.com', 'status':'available'}]))
        elif 'AuthName' in self.request.headers:
            hackerProfiles = Attendee.search_database({})
            listOfHackers = []
            for hackerProfile in hackerProfiles:
                _hacker = {'name':hackerProfile.name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'pictureURL':hackerProfile.pictureURL, 'status':hackerProfile.status}
                listOfHackers.append(_hacker)
            return self.write(json.dumps(listOfHackers))

        else:
            return self.write()    
        

class HackerHandler(MainHandler.BaseMobileHandler):

    def get(self):
        if self.request.headers['AuthName'] == 'test':
            return self.write(json.dumps({'name':'Jacob', 'email':'email@gmail.com', 'school':'uiuc', 'year':'senior', 'skills':'none', 'homebase':'1105', 'pictureURL':'url.com', 'status':'available'}))

        elif 'AuthName' in self.request.headers:
            if hackerProfile = Attendee.search_database({'userId':self.request.headers['AuthName']}).get()
                _hacker = {'name':hackerProfile.name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'type':'hacker', 'pictureURL':hackerProfile.pictureURL, 'status':hackerProfile.status}
                return self.write(json.dumps(_hacker))
            elif staffProfile = Admin.search_database({'userId':self.request.headers['AuthName']}).get():
                _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'type':'staff', 'pictureURL':staffProfile.pictureURL, 'status':staffProfile.status}
                return self.write(json.dumps(_staff))
            elif companyProfile = Sponsor.search_database({'userId':self.request.headers['AuthName']}).get():
                _companySponsor = {'name':_companySponsor.name, 'email':companyProfile.email, 'company':companyProfile.companyName, 'jobTitle':companyProfile.jobTitle, 'skills':companyProfile.skills, 'type':'company', 'pictureURL':companyProfile.pictureURL, 'status':companyProfile.status}
                return self.write(json.dumps(_companySponsor))
            else:
                return self.write()

        else:
            return self.write()

    def Post(self):
        if 'AuthName' in self.request.headers and self.request.headers['AuthName'] != 'test':
            updatedProfile = self.request.POST.items()
            updatedProfileDict = {}
            for _key,_value in updatedProfile:
                if _key != 'type':
                    updatedProfileDict[_key] = _value

            if updatedProfile['type'] == 'hacker':
                Attendee.update_search(updatedProfileDict, {'userId':self.request.headers['AuthName']})
            elif updatedProfile['type'] == 'staff':
                Admin.update_search(updatedProfileDict, {'userId':self.request.headers['AuthName']})
            elif updatedProfile['type'] == 'company':
                Sponsor.update_search(updatedProfileDict, {'userId':self.request.headers['AuthName']})


class CompaniesHandler(MainHandler.BaseMobileHandler):

    def get(self):
        if self.request.headers['AuthName'] == 'test':
            companyProfiles = {}

            for companyName in MobileConstants.COMPANY_NAMES:
                companyProfiles[companyName] = []
                companyProfile = Sponsor.search_database({'companyName':companyName})
                for _companyRep in companyProfile:
                    companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'jobTitle':_companyRep.jobTitle, 'skills':_companyRep.skills, 'pictureURL':_companyRep.pictureURL, 'status':_companyRep.status}
                    companyProfiles[companyName].append(companyRepProfile)
            return self.write(json.dumps(companyProfiles))

        elif 'AuthName' in self.request.headers:
            companyProfiles = {}

            for companyName in MobileConstants.COMPANY_NAMES:
                companyProfiles[companyName] = []
                companyProfile = Sponsor.search_database({'companyName':companyName})
                for _companyRep in companyProfile:
                    companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'jobTitle':_companyRep.jobTitle, 'skills':_companyRep.skills, 'pictureURL':_companyRep.pictureURL, 'status':_companyRep.status}
                    _list = companyProfiles[companyName]
                    _list.append(companyRepProfile)
            return self.write(json.dumps(companyProfiles))

        else:
            return self.write()


class SkillsHandler(MainHandler.BaseMobileHandler):

    '''

        @return A list of Skills that Hackers can have
    '''
    def get(self):
        return self.write(json.dumps(MobileConstants.SKILLS))
