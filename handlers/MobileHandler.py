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

def set_hacker_memcache():
    """Sets the 'hacker_mobile' key in the memcache"""
    # change to search for accepted hackers
    # hackers = Attendee.search_database({'isApproved':True})
    hackers = Attendee.search_database({})
    data = []
    for hackerProfile in hackers:
        name = ''
        if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
        if hackerProfile.nameLast: name+=hackerProfile.nameLast
        data.append({'name':name, 
                    'email':hackerProfile.email, 
                    'school':hackerProfile.school, 
                    'year':hackerProfile.year, 
                    'skills':hackerProfile.skills, 
                    'homebase':hackerProfile.homebase, 
                    'fb_url':hackerProfile.pictureURL, 
                    'status':hackerProfile.status, 
                    'database_key':str(hackerProfile.key),
                    'time':hackerProfile.updatedTime, 
                    'type':'hacker'})

    if not memcache.add('hacker_mobile', data, time=constants.MEMCACHE_TIMEOUT):
        logging.error('Memcache set failed for hacker_mobile.')

    return data

def set_staff_memcache():
    all_staff = Admin.search_database({})
    data = []

    for staff_profile in all_staff:
        data.append({'name':staff_profile.name, 
                    'email':staff_profile.email, 
                    'school':staff_profile.school, 
                    'year':staff_profile.year, 
                    'skills':staff_profile.skills, 
                    'homebase':staff_profile.homebase, 
                    'fb_url':staff_profile.pictureURL, 
                    'status':staff_profile.status, 
                    'database_key':str(staff_profile.key) , 
                    'time':staff_profile.updatedTime, 
                    'type':'staff'})

    if not memcache.add('staff_mobile', data, time=constants.MEMCACHE_TIMEOUT):
        logging.error('Memcache set failed for staff_mobile.')

    return data

def set_mentor_memcache():
    all_mentors = Sponsor.search_database({})
    data = []

    for mentor_profile in all_mentors:
        data.append({'name':mentor_profile.name,
                    'email':mentor_profile.email, 
                    'company':mentor_profile.company, 
                    'job_title':mentor_profile.jobTitle, 
                    'skills':mentor_profile.skills, 
                    'fb_url':mentor_profile.pictureURL, 
                    'status':mentor_profile.status, 
                    'database_key':str(mentor_profile.key) , 
                    'time':mentor_profile.updatedTime, 
                    'type':'mentor'})

    if not memcache.add('mentor_mobile', data, time=constants.MEMCACHE_TIMEOUT):
        logging.error('Memcache set failed for mentor_mobile.')

    return data

def set_all_mobile_memcache(hacker, mentor, staff):
    data = hacker+mentor+staff
    if not memcache.add('all', data, time.constants.MEMCACHE_TIMEOUT):
        logging.error('Memcache set failed.')

    return data

def get_people_memecache(table_key):
    """Gets the 'hackers' key from the memcache and updates the memcache if the key is not in the memcache"""

    all_data = None

    if table_key == 'all':
        all_data = memcache.get('all')
        if not all_data:
            hacker = self.set_hacker_memcache()
            mentor = self.set_mentor_memcache()
            staff = self.set_staff_memcache()

            all_data = set_all_mobile_memcache()

    elif table_key == 'hacker_mobile':
        all_data = memcache.get('hacker_mobile')

        if not all_data:
            all_data = set_hacker_memcache()

    elif table_key == 'mentor_mobile':
        all_data = memcache.get('mentor_mobile')

        if not all_data:
            all_data set_mentor_memcache()

    elif table_key == 'staff_mobile':
        all_data = memcache.get('staff_mobile')

        if not all_data:
            all_data = set_staff_memcache()

    stats = memcache.get_stats()
    logging.info('Hackers:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

    return all_data


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
                staffProfiles = get_people_memecache('staff_mobile')
                listOfStaff = []
                
                if not time:
                    for staffProfile in staffProfiles:
                        _staff = {'name':staffProfile.name, 
                        'email':staffProfile.email, 
                        'school':staffProfile.school, 
                        'year':staffProfile.year, 
                        'skills':staffProfile.skills, 
                        'homebase':staffProfile.homebase, 
                        'fb_url':staffProfile.pictureURL, 
                        'status':staffProfile.status, 
                        'database_key':str(staffProfile.key) , 
                        'time':staffProfile.updatedTime, 
                        'type':'staff'}
                        listOfStaff.append(_staff)
                else:
                    for staffProfile in staffProfiles:
                        if time >= staffProfile.updatedTime:
                            _staff = {'name':staffProfile.name, 
                            'email':staffProfile.email, 
                            'school':staffProfile.school, 
                            'year':staffProfile.year, 
                            'skills':staffProfile.skills, 
                            'homebase':staffProfile.homebase, 
                            'fb_url':staffProfile.pictureURL, 
                            'status':staffProfile.status, 
                            'database_key':str(staffProfile.key) , 
                            'time':staffProfile.updatedTime, 
                            'type':'staff'}
                            listOfStaff.append(_staff)
                return self.write(json.dumps(listOfStaff))
            
            if 'mentor' == params:
                companyProfiles = []
                
                companyProfile = get_people_memecache('mentor_mobile')
                for _companyRep in companyProfile:
                    if not time:
                        for _companyRep in companyProfile:
                            companyRepProfile = {'name':_companyRep.name,
                            'email':_companyRep.email, 
                            'company':_companyRep.company, 
                            'job_title':_companyRep.jobTitle, 
                            'skills':_companyRep.skills, 
                            'fb_url':_companyRep.pictureURL, 
                            'status':_companyRep.status, 
                            'database_key':str(_companyRep.key) , 
                            'time':_companyRep.updatedTime, 
                            'type':'mentor'}
                            companyProfiles.append(companyRepProfile)
                    else:
                        for _companyRep in companyProfile:
                            if time and time >= _companyRep.updatedTime:
                                companyRepProfile = {'name':_companyRep.name,
                                'email':_companyRep.email, 
                                'company':_companyRep.company, 
                                'job_title':_companyRep.jobTitle, 
                                'skills':_companyRep.skills, 
                                'fb_url':_companyRep.pictureURL, 
                                'status':_companyRep.status, 
                                'database_key':str(_companyRep.key) , 
                                'time':_companyRep.updatedTime, 
                                'type':'mentor'}
                                companyProfiles.append(companyRepProfile)
                return self.write(json.dumps(listOfMentors))
            
            # add search by accepting flag
            if 'hacker' == params:
                listOfHackers = []
                
                hackerProfiles = get_people_memecache('hacker_mobile')
                
                if not time:
                    for hackerProfile in hackerProfiles:
                        name = ''
                        if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                        if hackerProfile.nameLast: name+=hackerProfile.nameLast
                        _hacker = 
                            {'name':name, 
                            'email':hackerProfile.email, 
                            'school':hackerProfile.school, 
                            'year':hackerProfile.year, 
                            'skills':hackerProfile.skills, 
                            'homebase':hackerProfile.homebase, 
                            'fb_url':hackerProfile.pictureURL, 
                            'status':hackerProfile.status, 
                            'database_key':str(hackerProfile.key),
                            'time':hackerProfile.updatedTime, 
                            'type':'hacker'}
                        listOfHackers.append(_hacker)
                else:
                    for hackerProfile in hackerProfiles:
                        if time and time >= hackerProfile.updatedTime:
                            name = ''
                            if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                            if hackerProfile.nameLast: name+=hackerProfile.nameLast
                            _hacker = 
                            {'name':name, 
                            'email':hackerProfile.email, 
                            'school':hackerProfile.school, 
                            'year':hackerProfile.year, 
                            'skills':hackerProfile.skills, 
                            'homebase':hackerProfile.homebase, 
                            'fb_url':hackerProfile.pictureURL, 
                            'status':hackerProfile.status, 
                            'database_key':str(hackerProfile.key) ,
                            'time':hackerProfile.updatedTime, 
                            'type':'hacker'}
                            listOfHackers.append(_hacker)
                return self.write(json.dumps(listOfHackers))
            
            # TODO: need to revise and finish this function
            if 'key' == keyParams:
                profile = params['key'].get()
                for hackerProfile in profile:
                    name = ''
                    if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                    if hackerProfile.nameLast: name+=hackerProfile.nameLast
                    hackerProfile = [{'name':name, 
                    'email':hackerProfile.email, 
                    'school':hackerProfile.school, 
                    'year':hackerProfile.year, 
                    'skills':hackerProfile.skills, 
                    'homebase':hackerProfile.homebase, 
                    'picture_url':hackerProfile.pictureURL, 
                    'status':hackerProfile.status, 
                    'database_key':str(hackerProfile.key) ,
                    'time':hackerProfile.updatedTime}]
                    return self.write(json.dumps(hackerProfile))
        else:
            #get all hacker models
            listOfHackers = []
            
            hackerProfiles = get_people_memecache('hacker_mobile')
            if not time:
                for hackerProfile in hackerProfiles:
                    name = ''
                    if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                    if hackerProfile.nameLast: name+=hackerProfile.nameLast
                    _hacker = {'name':name, 
                    'email':hackerProfile.email, 
                    'school':hackerProfile.school, 
                    'year':hackerProfile.year, 
                    'skills':hackerProfile.skills, 
                    'homebase':hackerProfile.homebase, 
                    'fb_url':hackerProfile.pictureURL, 
                    'status':hackerProfile.status, 
                    'database_key':str(hackerProfile.key) ,
                    'time':hackerProfile.updatedTime, 
                    'type':'hacker'}
                    listOfHackers.append(_hacker)
            else:
                for hackerProfile in hackerProfiles:
                    if time and time >= hackerProfile.updatedTime:
                        name = ''
                        if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
                        if hackerProfile.nameLast: name+=hackerProfile.nameLast
                        _hacker = {'name':name, 
                        'email':hackerProfile.email, 
                        'school':hackerProfile.school, 
                        'year':hackerProfile.year, 
                        'skills':hackerProfile.skills, 
                        'homebase':hackerProfile.homebase, 
                        'fb_url':hackerProfile.pictureURL, 
                        'status':hackerProfile.status, 
                        'database_key':str(hackerProfile.key) ,
                        'time':hackerProfile.updatedTime, 
                        'type':'hacker'}
                        listOfHackers.append(_hacker)
            
            # get all staff models
            staffProfiles = get_people_memecache('staff_mobile')
            listOfStaff = []
            
            if not time:
                for staffProfile in staffProfiles:
                    _staff = {'name':staffProfile.name, 
                    'email':staffProfile.email, 
                    'school':staffProfile.school, 
                    'year':staffProfile.year, 
                    'skills':staffProfile.skills, 
                    'homebase':staffProfile.homebase, 
                    'fb_url':staffProfile.pictureURL, 
                    'status':staffProfile.status, 
                    'database_key':str(staffProfile.key) , 
                    'time':staffProfile.updatedTime, 
                    'type':'staff'}
                    listOfStaff.append(_staff)
            else:
                for staffProfile in staffProfiles:
                    if time >= staffProfile.updatedTime:
                        _staff = {'name':staffProfile.name, 
                        'email':staffProfile.email, 
                        'school':staffProfile.school, 
                        'year':staffProfile.year, 
                        'skills':staffProfile.skills, 
                        'homebase':staffProfile.homebase, 
                        'fb_url':staffProfile.pictureURL, 
                        'status':staffProfile.status, 
                        'database_key':str(staffProfile.key) , 
                        'time':staffProfile.updatedTime, 
                        'type':'staff'}
                        listOfStaff.append(_staff)
            
            # get all mentor models
            listOfMentors = []
            
            companyProfile = get_people_memecache('mentor_mobile')
            for _companyRep in companyProfile:
                if not time:
                    for _companyRep in companyProfile:
                        companyRepProfile = {'name':_companyRep.name,
                        'email':_companyRep.email, 
                        'company':_companyRep.company, 
                        'job_title':_companyRep.jobTitle, 
                        'skills':_companyRep.skills, 
                        'fb_url':_companyRep.pictureURL, 
                        'status':_companyRep.status, 
                        'database_key':str(_companyRep.key) , 
                        'time':_companyRep.updatedTime, 
                        'type':'mentor'}
                        listOfMentors.append(companyRepProfile)
                else:
                    for _companyRep in companyProfile:
                        if time and time >= _companyRep.updatedTime:
                            companyRepProfile = {'name':_companyRep.name,
                            'email':_companyRep.email, 
                            'company':_companyRep.company, 
                            'job_title':_companyRep.jobTitle, 
                            'skills':_companyRep.skills, 
                            'fb_url':_companyRep.pictureURL, 
                            'status':_companyRep.status, 
                            'database_key':str(_companyRep.key) , 
                            'time':_companyRep.updatedTime, 
                            'type':'mentor'}
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
