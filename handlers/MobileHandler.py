import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from db import MobileConstants
from db.Sponsor import Sponsor
from db.Admin import Admin
from db.Skills import Skills
from google.appengine.api import users, memcache
import json
import time


class ScheduleHandler(MainHandler.BaseMobileHandler):
    
    # Eventually we will have to pull this from a database when this is set up
    def get(self):
        return self.write(json.dumps(MobileConstants.SCHEDULE))


class SupportHandler(MainHandler.BaseMobileHandler):
    
    def get(self):
        return self.write(json.dumps(MobileConstants.SUPPORT))

class MapHandler(MainHandler.BaseMobileHandler):
    
    # Eventually we will have to pull this from a database when it is set up
    def get(self):
        return self.write(json.dumps(MobileConstants.MAP))


class NewsfeedHandler(MainHandler.BaseMobileHandler):
    '''
        
        @parameter before Top bound on the time for the NewsFeed
        @parameter since Bottom bound on the time for the NewsFeed (default should be your last time of the NewFeed card you have)
        @return The NewFeed models that are between the before and since parameters
        '''
    def get(self):
        mobile_last_updated = self.request.get('last_updated')
        
        if mobile_last_updated:
            pass
        else:
            empty_list = []
            list_of_news_feed_items = [{'subject':'iOS is better than Android', 'description':'First fake data for the app', 'time':77273243, 'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5', 'highlighted':[], 'emergency':True},
                                       {'description':'best hackathon ever! You wanted a longer description, so here is a much longer description', 'time':9923223, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[], 'emergency':False},
                                       {'description':'Rob love ios dev. Yes he does!', 'time':23423, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[], 'emergency':False},
                                       {'description':'Short weather. Georgia!', 'time':765524333, 'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5', 'highlighted':[[[0,5],[25,25,112]]], 'emergency':True},
                                       {'description':'WIFI Problems - Houston, we are experience Wifi problems on the first floor.', 'time':123412234, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[0,13],[25,25,112]]], 'emergency':False},
                                       {'description':'A spontaneous game of finger blasters is going to start in SC1404 in 5 minutes!', 'time':23452342, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[59,65],[139,0,12]]], 'emergency':False},
                                       {'description':'The first 100 people to tweet something to @hackillinois will win a Hack Illinois blanket', 'time':23453123, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[43,56],[139,0,12]]], 'emergency':False},
                                       {'description':'Rob is happy now', 'time':88923443, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[7,12],[139,0,0]]], 'emergency':False}]
                                       
            return self.write(json.dumps(list_of_news_feed_items))


class PersonHandler(MainHandler.BaseMobileHandler):
    
    def get(self):
        params = self.request.get('type')
        keyParams = self.request.get('key')
        time = self.request.get('last_updated')
        
        if params:
            if 'staff' == params:
                staffProfiles = Admin.search_database({})
                listOfStaff = []
                
                if not time:
                    for staffProfile in staffProfiles:
                        _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'fb_url':staffProfile.pictureURL, 'status':staffProfile.status, 'database_key':str(staffProfile.key) , 'time':staffProfile.updatedTime, 'type':'staff'}
                        listOfStaff.append(_staff)
                else:
                    for staffProfile in staffProfiles:
                        if time >= staffProfile.updatedTime:
                            _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'fb_url':staffProfile.pictureURL, 'status':staffProfile.status, 'database_key':str(staffProfile.key) , 'time':staffProfile.updatedTime, 'type':'staff'}
                            listOfStaff.append(_staff)
                return self.write(json.dumps(listOfStaff))
            
            if 'mentor' == params:
                companyProfiles = []
                
                companyProfile = Sponsor.search_database({})
                for _companyRep in companyProfile:
                    if not time:
                        for _companyRep in companyProfile:
                            companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'job_title':_companyRep.jobTitle, 'skills':_companyRep.skills, 'fb_url':_companyRep.pictureURL, 'status':_companyRep.status, 'database_key':str(_companyRep.key) , 'time':_companyRep.updatedTime, 'type':'mentor'}
                            companyProfiles.append(companyRepProfile)
                    else:
                        for _companyRep in companyProfile:
                            if time and time >= _companyRep.updatedTime:
                                companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'job_title':_companyRep.jobTitle, 'skills':_companyRep.skills, 'fb_url':_companyRep.pictureURL, 'status':_companyRep.status, 'database_key':str(_companyRep.key) , 'time':_companyRep.updatedTime, 'type':'mentor'}
                                companyProfiles.append(companyRepProfile)
                return self.write(json.dumps(listOfMentors))
            
            # add search by accepting flag
            if 'hacker' == params:
                listOfHackers = []
                
                hackerProfiles = Attendee.search_database({})
                
                if not time:
                    for hackerProfile in hackerProfiles:
                        name = ''
                        if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                        if hackerProfile.nameLast: name+=hackerProfile.nameLast
                        _hacker = {'name':name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'fb_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':str(hackerProfile.key) ,'time':hackerProfile.updatedTime, 'type':'hacker'}
                        listOfHackers.append(_hacker)
                else:
                    for hackerProfile in hackerProfiles:
                        if time and time >= hackerProfile.updatedTime:
                            name = ''
                            if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                            if hackerProfile.nameLast: name+=hackerProfile.nameLast
                            _hacker = {'name':name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'fb_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':str(hackerProfile.key) ,'time':hackerProfile.updatedTime, 'type':'hacker'}
                            listOfHackers.append(_hacker)
                return self.write(json.dumps(listOfHackers))
            
            if 'key' == keyParams:
                profile = params['key'].get()
                for hackerProfile in profile:
                    name = ''
                    if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                    if hackerProfile.nameLast: name+=hackerProfile.nameLast
                    hackerProfile = [{'name':name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'picture_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':str(hackerProfile.key) ,'time':hackerProfile.updatedTime}]
                    return self.write(json.dumps(hackerProfile))
        else:
            #get all hacker models
            listOfHackers = []
            
            hackerProfiles = Attendee.search_database({})
            if not time:
                for hackerProfile in hackerProfiles:
                    name = ''
                    if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                    if hackerProfile.nameLast: name+=hackerProfile.nameLast
                    _hacker = {'name':name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'fb_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':str(hackerProfile.key) ,'time':hackerProfile.updatedTime, 'type':'hacker'}
                    listOfHackers.append(_hacker)
            else:
                for hackerProfile in hackerProfiles:
                    if time and time >= hackerProfile.updatedTime:
                        name = ''
                        if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                        if hackerProfile.nameLast: name+=hackerProfile.nameLast
                        _hacker = {'name':name, 'email':hackerProfile.email, 'school':hackerProfile.school, 'year':hackerProfile.year, 'skills':hackerProfile.skills, 'homebase':hackerProfile.homebase, 'fb_url':hackerProfile.pictureURL, 'status':hackerProfile.status, 'database_key':str(hackerProfile.key) ,'time':hackerProfile.updatedTime, 'type':'hacker'}
                        listOfHackers.append(_hacker)
            
            # get all staff models
            staffProfiles = Admin.search_database({})
            listOfStaff = []
            
            if not time:
                for staffProfile in staffProfiles:
                    _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'fb_url':staffProfile.pictureURL, 'status':staffProfile.status, 'database_key':str(staffProfile.key) , 'time':staffProfile.updatedTime, 'type':'staff'}
                    listOfStaff.append(_staff)
            else:
                for staffProfile in staffProfiles:
                    if time >= staffProfile.updatedTime:
                        _staff = {'name':staffProfile.name, 'email':staffProfile.email, 'school':staffProfile.school, 'year':staffProfile.year, 'skills':staffProfile.skills, 'homebase':staffProfile.homebase, 'fb_url':staffProfile.pictureURL, 'status':staffProfile.status, 'database_key':str(staffProfile.key) , 'time':staffProfile.updatedTime, 'type':'staff'}
                        listOfStaff.append(_staff)
            
            # get all mentor models
            listOfMentors = []
            
            companyProfile = Sponsor.search_database({})
            for _companyRep in companyProfile:
                if not time:
                    for _companyRep in companyProfile:
                        companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'job_title':_companyRep.jobTitle, 'skills':_companyRep.skills, 'fb_url':_companyRep.pictureURL, 'status':_companyRep.status, 'database_key':str(_companyRep.key) , 'time':_companyRep.updatedTime, 'type':'mentor'}
                        listOfMentors.append(companyRepProfile)
                else:
                    for _companyRep in companyProfile:
                        if time and time >= _companyRep.updatedTime:
                            companyRepProfile = {'email':_companyRep.email, 'company':_companyRep.company, 'job_title':_companyRep.jobTitle, 'skills':_companyRep.skills, 'fb_url':_companyRep.pictureURL, 'status':_companyRep.status, 'database_key':str(_companyRep.key) , 'time':_companyRep.updatedTime, 'type':'mentor'}
                            listOfMentors.append(companyRepProfile)
            
            
            
            return self.write(json.dumps(listOfMentors+listOfStaff+listOfHackers))
    
    
    def post(self):
        user = users.get_current_user()
        params = self.request.boby()
        
        updatedProfile = json.loads(params)
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
            
            return self.write(json.dumps({'message':'Updated Profile'}))
        else:
            return self.write(json.dumps({'message':'No user'}))

# DONE
class SkillsHandler(MainHandler.BaseMobileHandler):
    def get(self):
        querySkills = Skills.search_database({})
        listOfSkills = []
        
        for skill in querySkills:
            skillDict = {'name':skill.name, 'alias':skill.alias, 'tags':skill.tags}
            listOfSkills.append(skillDict)
        
        return self.write(json.dumps(listOfSkills))


class LoginHandler(MainHandler.BaseMobileHandler):
    def get(self):
        user = users.get_current_user()
        if not user: return self.write(json.dumps({'message':'No user'}))
        
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
        
        self.write(json.dumps([profile]))
