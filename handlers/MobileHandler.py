import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from db.mobile import MobileConstants
from db.Sponsor import Sponsor
from db.Admin import Admin
from google.appengine.api import users, memcache
import json
import time


class ScheduleHandler(MainHandler.BaseMobileHandler):

    def get(self):
        return self.write(json.dumps([{'event name':'First Event' ,'description':'Blast Off' ,'location':'room #1' ,'time':'12:00pm'}]))


class SupportHandler(MainHandler.BaseMobileHandler):

    def get(self):
        return self.write(json.dumps(MobileConstants.SUPPORT))


class NewsfeedHandler(MainHandler.BaseMobileHandler):

    '''

        @parameter before Top bound on the time for the NewsFeed
        @parameter since Bottom bound on the time for the NewsFeed (default should be your last time of the NewFeed card you have)
        @return The NewFeed models that are between the before and since parameters
    '''
    def get(self):
        return self.write(json.dumps([{'event name':'first event of HackIllinois' ,'location':'room #1' ,'time':'1:00pm'}]))

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
        

class PersonHandler(MainHandler.BaseMobileHandler):

    def get(self):
        params = self.request.POST.items()

        if 'type' in params:
            if 'staff' == params['type']:
                staffProfiles = Staff.search_database({})
                listOfStaff = []
                for staffProfile in staffProfiles:
                    if params['last_updated'] >= staffProfile.updatedTime:
                        _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'picture_url':staffProfile.pictureURL, 'status':staffProfile.status, 'database_key':staffProfile.key , 'time':_companyRep.updatedTime}
            
            if 'mentor' in params['type']:
                companyProfiles = {}

                for companyName in MobileConstants.COMPANY_NAMES:
                    companyProfiles[companyName] = []
                    companyProfile = Sponsor.search_database({'companyName':companyName})
                    for _companyRep in companyProfile:
                        if params['last_updated'] >= _companyRep.updatedTime:
                            companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'job_title':_companyRep.jobTitle, 'skills':_companyRep.skills, 'picture_url':_companyRep.pictureURL, 'status':_companyRep.status, 'database_key':_companyRep.key , 'time':_companyRep.updatedTime}
                            companyProfiles[companyName].append(companyRepProfile)
                return self.write(json.dumps(companyProfiles))

            # add search by accepting flag
            if 'hacker' in params['type']:
                hackerProfiles = Attendee.search_database({})
                listOfHackers = []
                for hackerProfile in hackerProfiles:
                    if params['last_updated'] >= hackerProfile.updatedTime:
                        _hacker = {'name':hackerProfile.name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'picture_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':hackerProfile.key ,'time':_companyRep.updatedTime}
                        listOfHackers.append(_hacker)
                return self.write(json.dumps(listOfHackers))
        elif 'key' in params:
            profile = params['key'].get()
            for hackerProfile in profile:
                hackerProfile = {'name':hackerProfile.name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'picture_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':hackerProfile.key ,'time':_companyRep.updatedTime}
                return self.write(json.dumps(hackerProfile))

    def post(self):
        user = users.get_current_user()
        params = self.request.POST.items()

        updatedProfileDict = {}
        for _key,_value in updatedProfile:
            updatedProfileDict[_key] = _value

        if user:
            hackerProfile = Attendee.search_database({'userId':user.user_id()}).get()
            staffProfile = Admin.search_database({'userId':user.user_id()}).get()
            companyProfile = Sponsor.search_database({'userId':user.user_id()}).get()

            if hackerProfile:
                Attendee.update_search(updatedProfileDict, {'userId':user.user_id()})
            elif staffProfile:
                Admin.update_search(updatedProfileDict, {'userId':user.user_id()})
            elif companyProfile:
                Sponsor.update_search(updatedProfileDict, {'userId':user.user_id()})
            
            return self.abort(200, detail='Updated Profile')
        else:
            return self.abort(500, detail='No user')


class SkillsHandler(MainHandler.BaseMobileHandler):

    '''

        @return A list of Skills that Hackers can have
    '''
    def get(self):
        return self.write(json.dumps(MobileConstants.SKILLS))

class LoginHandler(MainHandler.BaseMobileHandler):
    def get(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not in database')

        hackerProfile = Attendee.search_database({'userId':user.user_id()}).get()
        staffProfile = Admin.search_database({'userId':user.user_id()}).get()
        companyProfile = Sponsor.search_database({'userId':user.user_id()}).get()
        profile = {}
        
        if hackerProfile:
            profile = {'name':hackerProfile.name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'picture_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':hackerProfile.key ,'time':_companyRep.updatedTime}
        elif staffProfile:
            profile = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'picture_url':staffProfile.pictureURL, 'status':staffProfile.status, 'database_key':staffProfile.key , 'time':_companyRep.updatedTime}
        elif companyProfile:
            profile = {'email':_companyRep.email, 'company':_companyRep.company, 'job_title':_companyRep.jobTitle, 'skills':_companyRep.skills, 'picture_url':_companyRep.pictureURL, 'status':_companyRep.status, 'database_key':_companyRep.key , 'time':_companyRep.updatedTime}

        self.write(json.dumps(profile))
