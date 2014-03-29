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

def get_hacker_data():
    """Sets the 'hacker_mobile' key in the memcache"""
    # change to search for accepted hackers
    # hackers = Attendee.search_database({'isApproved':True})
    hackers = Attendee.search_database({})
    data = []
    for hackerProfile in hackers:
        name = ''
        if hackerProfile.nameFirst: 
            name+=hackerProfile.nameFirst + ' '
        if hackerProfile.nameLast: 
            name+=hackerProfile.nameLast
        data.append({'name':name, 
                    'email':hackerProfile.email, 
                    'school':hackerProfile.school, 
                    'year':hackerProfile.year, 
                    'skills':hackerProfile.skills, 
                    'homebase':hackerProfile.homebase, 
                    'fb_url':hackerProfile.pictureURL, 
                    'status':hackerProfile.status, 
                    'database_key':hackerProfile.email,
                    'time':hackerProfile.updatedTime, 
                    'type':'hacker'})

    return data

def get_staff_data():
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
                    'database_key':staff_profile.email, 
                    'time':staff_profile.updatedTime, 
                    'type':'staff'})

    return data

def get_mentor_data():
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
                    'database_key':mentor_profile.email, 
                    'time':mentor_profile.updatedTime, 
                    'type':'mentor'})

    # This is added to give Rob fake mentor data and act in the same way as going through memcache
    data = MobileConstants.FAKE_MENTOR_DATA

    return data

def set_all_mobile_memcache():
    hacker = get_hacker_data()
    mentor = get_mentor_data()
    staff = get_staff_data()

    data = hacker+mentor+staff
    if not memcache.add('all', data, time=constants.MOBILE_MEMCACHE_TIMEOUT):
        logging.error('Memcache set failed.')

    return data

def get_people_memecache(table_key):
    """Gets the 'hackers' key from the memcache and updates the memcache if the key is not in the memcache"""

    all_data = None
    return_data = []

    # get memcache data
    all_data = memcache.get('all')

    if not all_data:
        all_data = set_all_mobile_memcache()

    stats = memcache.get_stats()
    logging.info('Hackers:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

    # set up return data list depending on what is requested
    for data in all_data:
        if (table_key == 'hacker_mobile') and (data['type'] == 'hacker'):
            return_data.append(data)
        elif (table_key == 'mentor_mobile') and (data['type'] == 'mentor'):
            return_data.append(data)
        elif (table_key == 'staff_mobile') and (data['type'] == 'staff'):
            return_data.append(data)
        elif (table_key == 'all'):
            return_data.append(data)

    return return_data


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
                listOfStaff = get_people_memecache('staff_mobile')
                return self.write(json.dumps(listOfStaff))
            
            if 'mentor' == params:
                listOfMentors = get_people_memecache('mentor_mobile')
                return self.write(json.dumps(listOfMentors))
            
            # add search by accepting flag
            if 'hacker' == params:
                listOfHackers = get_people_memecache('hacker_mobile')
                return self.write(json.dumps(listOfHackers))
            
            if 'key' == keyParams:
                profile = params['key'].get()

                allProfiles = get_people_memecache('all')

                for personProfile in allProfiles:
                    if personProfile.email == profile:
                        return self.write(json.dumps([personProfile]))

        else:
            #get all models
            listOfEveryone = get_people_memecache('all')
            return self.write(json.dumps(listOfEveryone))
    
    
    def post(self):
        if 'Email' in self.request.headers:
            email = self.request.headers['Email']
            email = email.lower()
        else:
            return self.write(json.dumps({'message':'No userId'}))

        params = self.request.boby()
        
        updatedProfile = json.loads(params)
        updatedProfileDict = {}
        updatedKeys = []
        for _key,_value in updatedProfile:
            updatedProfileDict[_key] = _value
            updatedKeys.append(_key)
        
        if email:
            hackerProfile = Attendee.search_database({'email_lower':email}).get()
            staffProfile = Admin.search_database({'email_lower':email}).get()
            companyProfile = Sponsor.search_database({'email_lower':email}).get()
            
            if hackerProfile:
                # update datastore
                Attendee.update_search(updatedProfileDict, {'email_lower':email})

                # update memcache
                all_hacker_profiles = get_people_memecache('all')
                for memcache_hacker_profile in all_hacker_profiles:
                    if memcache_hacker_profile.email == hackerProfile.email:
                        if 'skills' in updatedKeys:
                            memcache_hacker_profile.skills = updatedProfileDict['skills']
                        elif 'homebase' in updatedKeys:
                            memcache_hacker_profile.homebase = updatedProfileDict['homebase']
                if not memcache.replace('all', all_hacker_profiles,time=constants.MOBILE_MEMCACHE_TIMEOUT):
                    logging.error('Memcache set failed for all.')

            elif staffProfile:
                # update datastore
                Admin.update_search(updatedProfileDict, {'email_lower':email})

                #update memcache
                all_staff_profiles = get_people_memecache('all')
                for memcache_staff_profile in all_staff_profiles:
                    if memcache_staff_profile.email == staffProfile.email:
                        if 'skills' in updatedKeys:
                            memcache_staff_profile.skills = updatedProfileDict['skills']
                        elif 'homebase' in updatedKeys:
                            memcache_staff_profile.homebase = updatedProfileDict['homebase']
                if not memcache.replace('all', all_staff_profiles, time=constants.MOBILE_MEMCACHE_TIMEOUT):
                    logging.error('Memcache set failed for all')

            elif companyProfile:
                # update datastore
                Sponsor.update_search(updatedProfileDict, {'email_lower':email})

                # update memcache
                all_mentor_profiles = get_people_memecache('all')
                for memcache_mentor_profile in all_mentor_profiles:
                    if memcache_mentor_profile.email == companyProfile.email:
                        if 'skills' in updatedKeys:
                            memcache_mentor_profile.skills = updatedProfileDict['skills']
                        elif 'homebase' in updatedKeys:
                            memcache_mentor_profile.homebase = updatedProfileDict['homebase']
                        elif 'status' in updatedKeys:
                            memcache_mentor_profile.status = updatedKeys['status']
                if not memcache.replace('all', all_mentor_profiles, time=constants.MOBILE_MEMCACHE_TIMEOUT):
                    logging.error('Memcache set failed for all')
            
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
        email = None
        if 'Email' in self.request.headers:
            email = self.request.headers['Email']
            email = email.lower()
        else:
            return self.write(json.dumps({'message':'No userId'}))

        # filter by accepted and attending later on
        hackerProfile = Attendee.search_database({'email_lower':email}).get()
        staffProfile = Admin.search_database({'email_lower':email}).get()
        mentorProfile = Sponsor.search_database({'email_lower':email}).get()

        if not hackerProfile and staffProfile and mentorProfile: 
            return self.write(json.dumps({'message':'No user'}))   
        
        profile = {}
        
        if hackerProfile:
            name = ''
            if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
            if hackerProfile.nameLast: name+=hackerProfile.nameLast
            profile = {'name':hackerProfile.name, 
            'email':hackerProfile.email, 
            'school':hackerProfile.school, 
            'year':hackerProfile.year,
            'skills':hackerProfile.skills, 
            'homebase':hackerProfile.homebase, 
            'fb_url':hackerProfile.pictureURL, 
            'status':hackerProfile.status, 
            'database_key':hackerProfile.email ,
            'time':hackerProfile.updatedTime,
            'type':'hacker'}
        elif staffProfile:
            profile = {'name':staffProfile.name, 
            'email':staffProfile.email, 
            'school':staffProfile.school, 
            'year':staffProfile.year,
            'skills':staffProfile.skills, 
            'homebase':staffProfile.homebase, 
            'fb_url':staffProfile.pictureURL, 
            'status':staffProfile.status, 
            'database_key':staffProfile.email , 
            'time':staffProfile.updatedTime,
            'type':'staff'}
        elif mentorProfile:
            profile = {'name':'mentorProfile.name',
            'email':'mentorProfile.email@gmail.com', 
            'company':'mentorProfile.company', 
            'job_title':'mentorProfile.jobTitle', 
            'skills':['mentorProfile.skills'], 
            'fb_url':'mentorProfile.pictureURL', 
            'status':'mentorProfile.status', 
            'database_key':'mentorProfile.email' , 
            'time':'mentorProfile.updatedTime',
            'type':'mentor'}

            # profile = {'name':mentorProfile.name,
            # 'email':mentorProfile.email, 
            # 'company':mentorProfile.company, 
            # 'job_title':mentorProfile.jobTitle, 
            # 'skills':mentorProfile.skills, 
            # 'fb_url':mentorProfile.pictureURL, 
            # 'status':mentorProfile.status, 
            # 'database_key':mentorProfile.email , 
            # 'time':mentorProfile.updatedTime,
            # 'type':'mentor'}
        
        self.write(json.dumps([profile]))
