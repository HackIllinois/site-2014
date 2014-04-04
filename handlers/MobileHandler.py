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

# def filter_status(profile_status_list):
#     if len(profile_status_list) <= 3:
#         return profile_status_list
#     else:
#         most_recent_status = None
#         status_list = []
#         x = 0
#         while x < 3:
#             for status_dict in profile_status_list:
#                 if most_recent_status == None:
#                     most_recent_status = item
#                 elif most_recent_status['time'] < item['time']:
#                     third_most_recent_status = item

#                 status_list.remove(third_most_recent_status)
#                 status_list.append(status_dict)
#             x = x + 1
#         return status_list


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def check_email_for_login(email):
    if not email:
        return False

    hackerProfile = Attendee.search_database({'userEmail':email}).get()
    staffProfile = Admin.search_database({'email':email}).get()
    mentorProfile = Sponsor.search_database({'email':email}).get()
    
    if hackerProfile or staffProfile or mentorProfile: 
        return True
    else:
        return False

def get_hacker_data():
    """Sets the 'hacker_mobile' key in the memcache"""
    # hackers = Attendee.query(Attendee.approvalStatus.status == "Rsvp Coming", ancestor=Attendee.get_default_event_parent_key())
    hackers = Attendee.search_database({})
    data = []
    for hackerProfile in hackers:
        name = ''
        if hackerProfile.nameFirst: 
            name+=hackerProfile.nameFirst + ' '
        if hackerProfile.nameLast: 
            name+=hackerProfile.nameLast
        profile = {'email':hackerProfile.email, 
                    'school':hackerProfile.school, 
                    'year':hackerProfile.year, 
                    'homebase':hackerProfile.homebase, 
                    'fb_url':hackerProfile.pictureURL, 
                    'database_key':hackerProfile.database_key,
                    'time':hackerProfile.updatedTime, 
                    'type':'hacker'}

        if hackerProfile.skills:
            if hackerProfile.skills[0] != "":
                profile['skills'] = hackerProfile.skills
            else:
                profile['skills'] = []
        else:
            profile['skills'] = []
        
        if hackerProfile.status_list:
            if hackerProfile.status_list[0] != "":
                profile['status'] = hackerProfile.status_list
            else:
                profile['status'] = []
        else:
            profile['status'] = []

        # if len(hackerProfile.status_list) <= 3:
        #     profile['status'] = hackerProfile.status_list
        # else:
            # filter the 3 most recent and add them into the profile

        if name != "":
            profile['name'] = name
            data.append(profile)

    return data[:800]

def get_staff_data():
    all_staff = Admin.search_database({})
    data = []

    for staff_profile in all_staff:
        profile = {'name':staff_profile.name, 
                    'email':staff_profile.email, 
                    'company':staff_profile.companyName,
                    'job_title':staff_profile.jobTitle,
                    'year':staff_profile.year, 
                    'homebase':staff_profile.homebase, 
                    'fb_url':staff_profile.pictureURL, 
                    'database_key':staff_profile.database_key, 
                    'time':staff_profile.updatedTime, 
                    'type':personType}
        if staff_profile.skills:
            if staff_profile.skills[0] != "":
                profile['skills'] = staff_profile.skills
            else:
                profile['skills'] = []
        else:
            profile['skills'] = []

        if staff_profile.status_list:
            if staff_profile.status_list[0] != "":
                profile['status'] = staff_profile.status_list
            else:
                profile['status'] = []
        else:
            profile['status'] = []

        # if len(staff_profile.status_list) <= 3:
        #     profile['status'] = staff_profile.status
        # else:
            # filter the 3 most recent and add them into the profile

        if staff_profile.name != "":
            data.append(profile)

    return data

def get_mentor_data():
    all_mentors = Sponsor.search_database({})
    data = []

    for mentor_profile in all_mentors:
        profile = {'name':mentor_profile.name,
                    'email':mentor_profile.email, 
                    'company':mentor_profile.companyName, 
                    'job_title':mentor_profile.jobTitle, 
                    'fb_url':mentor_profile.pictureURL, 
                    'database_key':mentor_profile.database_key, 
                    'time':mentor_profile.updatedTime, 
                    'type':'mentor'}

        if mentor_profile.skills:            
            if mentor_profile.skills[0] != "":
                profile['skills'] = mentor_profile.skills
            else:
                profile['skills'] = []
        else:
            profile['skills'] = []

        if mentor_profile.status_list:
            if mentor_profile.status_list[0] != "":
                profile['status'] = mentor_profile.status_list
            else:
                profile['status'] = []
        else:
            profile['status'] = []

        # if len(mentor_profile.status_list) <= 3:
        #     profile['status'] = mentor_profile.status_list
        # else
            # filter the 3 most recent and add them into the profile


        data.append(profile)

    return data

def set_all_mobile_memcache():
    hacker = get_hacker_data()
    mentor = get_mentor_data()
    staff = get_staff_data()

    data = hacker+mentor+staff
    if not memcache.set('all', data, time=constants.MOBILE_MEMCACHE_TIMEOUT):
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
        valid_email = False
        if 'Email' in self.request.headers:
            valid_email = check_email_for_login(self.request.headers['Email'])

        if not valid_email:
            return self.write(json.dumps({}))

        return self.write(json.dumps(MobileConstants.SCHEDULE))


class SupportHandler(MainHandler.BaseMobileHandler):
    
    def get(self):
        valid_email = False
        if 'Email' in self.request.headers:
            valid_email = check_email_for_login(self.request.headers['Email'])

        if not valid_email:
            return self.write(json.dumps({}))

        return self.write(json.dumps(MobileConstants.SUPPORT))

class MapHandler(MainHandler.BaseMobileHandler):
    
    # Eventually we will have to pull this from a database when it is set up
    def get(self):
        valid_email = False
        if 'Email' in self.request.headers:
            valid_email = check_email_for_login(self.request.headers['Email'])

        if not valid_email:
            return self.write(json.dumps([]))

        return self.write(json.dumps(MobileConstants.MAP))


class NewsfeedHandler(MainHandler.BaseMobileHandler):
    '''
        
        @parameter before Top bound on the time for the NewsFeed
        @parameter since Bottom bound on the time for the NewsFeed (default should be your last time of the NewFeed card you have)
        @return The NewFeed models that are between the before and since parameters
        '''
    def get(self):
        valid_email = False
        if 'Email' in self.request.headers:
            valid_email = check_email_for_login(self.request.headers['Email'])

        if not valid_email:
            return self.write(json.dumps([]))
        
        empty_list = []
        list_of_news_feed_items = [{'description':'ANNOUNCEMENT - Interactive Itelligence is hiring! Check out our jobs at inin.jobs.', 'time':1396269004, 'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5', 'highlighted':[[[0,12],[30,75,102]]], 'emergency':False},
                                   {'description':'WIFI Problems - Houston, we are experience Wifi problems on the first floor.', 'time':1396269010, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[0,13],[167,65,46]]], 'emergency':True},
                                   {'description':'A spontaneous game of finger blasters is going to start in SC1404 in 5 minutes!', 'time':1396269923, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[59,65],[19,38,51]]], 'emergency':False},
                                   {'description':'The first 100 people to tweet something to @hackillinois will win a Hack Illinois blanket', 'time':1396269876, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[43,56],[19,38,51]]], 'emergency':False}]
                                   # {'description':'', 'time':9923223, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[], 'emergency':False},
                                   # {'description':'', 'time':23423, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[], 'emergency':False},
                                   # {'description':'', 'time':765524333, 'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5', 'highlighted':[[[0,5],[25,25,112]]], 'emergency':True},
                                   # {'description':'', 'time':88923443, 'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png', 'highlighted':[[[7,12],[139,0,0]]], 'emergency':False}]
                                   
        return self.write(json.dumps(list_of_news_feed_items))


class PersonHandler(MainHandler.BaseMobileHandler):
    
    def get(self):
        valid_email = False
        if 'Email' in self.request.headers:
            valid_email = check_email_for_login(self.request.headers['Email'])

        if not valid_email:
            return self.write(json.dumps([]))
        
        time = self.request.get('last_updated')
        
        if self.request.get('type'):
            params = self.request.get('type')
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
            
        elif self.request.get('key'):
            keyParams = self.request.get('key')

            person = Attendee.search_database({'database_key':keyParams})
            if not person:
                person = Sponsor.search_database({'database_key':keyParams})
            if not person:
                person = Admin.search_database({'database_key':keyParams})
            if not person: 
                return self.write(json.dumps([]))

            return self.write(json.dumps([person]))

            
        else:
            #get all models
            listOfEveryone = get_people_memecache('all')

            return self.write(json.dumps(listOfEveryone))
    
    
    def post(self):
        if 'Email' in self.request.headers:
            email = self.request.headers['Email']
            # email = email.lower()
        else:
            return self.write(json.dumps({'message':'No userId'}))

        params = self.request.body
        updatedProfile = None

        try:
            updatedProfile = json.loads(params, object_hook=_decode_dict)
        except ValueError, e:
            return self.write(json.dumps({'message':'Invalid JSON'}))
            
        updatedProfileDict = {}
        updatedKeys = []
        for _key in updatedProfile:
            if _key == 'status':
                updatedProfileDict['status_list'] = updatedProfile[_key]
            elif _key == 'fb_url':
                updatedProfileDict['pictureURL'] = updatedProfile[_key]
            else:
                updatedProfileDict[_key] = updatedProfile[_key]
            updatedKeys.append(_key)
        
        if email:
            hackerProfile = Attendee.search_database({'userEmail':email}).get()
            staffProfile = Admin.search_database({'email':email}).get()
            companyProfile = Sponsor.search_database({'email':email}).get()
            
            if hackerProfile:
                # update datastore
                Attendee.update_search(updatedProfileDict, {'userEmail':email})

            elif staffProfile:
                # update datastore
                Admin.update_search(updatedProfileDict, {'email':email})

            elif companyProfile:
                # update datastore
                Sponsor.update_search(updatedProfileDict, {'email':email})

            # update memcache
            all_profiles = get_people_memecache('all')
            for memcache_profile in all_profiles:
                if memcache_profile['email'] == email:
                    if 'skills' in updatedKeys:
                        if isinstance(updatedProfileDict['skills'],list) and all(isinstance(idx, str) for idx in updatedProfileDict['skills']):
                            memcache_profile['skills'] = updatedProfileDict['skills']
                        else:
                            return self.write(json.dumps({'message':'Invalid skills'}))
                    elif 'homebase' in updatedKeys:
                        if isinstance(updatedProfileDict['homebase'],str):
                            memcache_profile['homebase'] = updatedProfileDict['homebase']
                        else:
                            return self.write(json.dumps({'message':'Invalid homebase'}))
                    elif 'fb_url' in updatedKeys:
                        if isinstance(updatedProfileDict['pictureURL'],str):
                            memcache_profile['fb_url'] =  updatedProfileDict['pictureURL']
                        else:
                            return self.write(json.dumps({'message':'Invalid fb_url'}))
                    elif 'status' in updatedKeys:
                        if isinstance(updatedProfileDict['status_list'],list) and all(isinstance(idx,dict) for idx in updatedProfileDict['status_list']):
                            memcache_profile['status'] = updatedProfileDict['status_list']
                        else:
                            return self.write(json.dumps({'message':'Invalid status'}))
                    
            if memcache.replace('all', all_profiles, time=constants.MOBILE_MEMCACHE_TIMEOUT):
                return self.write(json.dumps({'message':'Updated Profile'}))
            else:
                logging.error('Memcache set failed for all')

                return self.write(json.dumps({'message':'Memcache replace failed'}))

        else:
            return self.write(json.dumps({'message':'No user'}))

# DONE
class SkillsHandler(MainHandler.BaseMobileHandler):
    def get(self):
        valid_email = False
        if 'Email' in self.request.headers:
            valid_email = check_email_for_login(self.request.headers['Email'])

        if not valid_email:
            return self.write(json.dumps([]))

        querySkills = Skills.search_database({})
        listOfSkills = []
        
        for skill in querySkills:
            skillDict = {'name':skill.name}
            if len(skill.alias) == 1:
                if (skill.alias[0] != "") and (skill.alias[0] != " "):
                    skillDict['alias'] = skill.alias
            else:
                skillDict['alias'] = []
            
            if len(skill.tags) == 1:
                if (skill.tags[0] != "") and (skill.tags[0] != " "):
                    skillDict['tags'] = skill.tags
            else:
                skillDict['tags'] = []

            listOfSkills.append(skillDict)
        
        return self.write(json.dumps(listOfSkills))


class LoginHandler(MainHandler.BaseMobileHandler):
    def get(self):
        email = None
        if 'Email' in self.request.headers:
            email = self.request.headers['Email']
            # email = email.lower()
        else:
            return self.write(json.dumps([]))

        # filter by accepted and attending later on
        hackerProfile = Attendee.search_database({'userEmail':email}).get()
        staffProfile = Admin.search_database({'email':email}).get()
        mentorProfile = Sponsor.search_database({'email':email}).get()
        
        list_profile = []
        
        if hackerProfile:
            name = ''
            if hackerProfile.nameFirst: name+=hackerProfile.nameFirst + ' '
            if hackerProfile.nameLast: name+=hackerProfile.nameLast
            profile = {'name':name, 
            'email':hackerProfile.email, 
            'school':hackerProfile.school, 
            'year':hackerProfile.year,
            'homebase':hackerProfile.homebase, 
            'fb_url':hackerProfile.pictureURL, 
            'status':hackerProfile.status_list, 
            'database_key':hackerProfile.database_key ,
            'time':hackerProfile.updatedTime,
            'type':'hacker'}

            if hackerProfile.skills:
                if hackerProfile.skills[0] != "":
                    profile['skills'] = hackerProfile.skills
                else:
                    profile['skills'] = []
            else:
                profile['skills'] = []

            if hackerProfile.status_list:
                if hackerProfile.status_list[0] != "":
                    profile['status'] = hackerProfile.status_list
                else:
                    profile['status'] = []
            else:
                profile['status'] = []


            list_profile.append(profile)
        elif staffProfile:
            profile = {'name':staffProfile.name, 
            'email':staffProfile.email, 
            'company':staffProfile.companyName,
            'job_title':staffProfile.jobTitle,
            'year':staffProfile.year,
            'homebase':staffProfile.homebase, 
            'fb_url':staffProfile.pictureURL, 
            'status':staffProfile.status_list, 
            'database_key':staffProfile.database_key, 
            'time':staffProfile.updatedTime,
            'type':staffProfile.personType}

            if staffProfile.skills:
                if staffProfile.skills[0] != "":
                    profile['skills'] = staffProfile.skills
                else:
                    profile['skills'] = []
            else:
                profile['skills'] = []

            if staffProfile.status_list:
                if staffProfile.status_list[0] != "":
                    profile['status'] = staffProfile.status_list
                else:
                    profile['status'] = []
            else:
                profile['status'] = []

            list_profile.append(profile)
        elif mentorProfile:
            profile = {'name':mentorProfile.name,
            'email':mentorProfile.email, 
            'company':mentorProfile.companyName, 
            'job_title':mentorProfile.jobTitle, 
            'fb_url':mentorProfile.pictureURL, 
            'status':mentorProfile.status_list, 
            'database_key':mentorProfile.database_key , 
            'time':mentorProfile.updatedTime,
            'type':'mentor'}
            
            if mentorProfile.skills:
                if mentorProfile.skills[0] != "":
                    profile['skills'] = mentorProfile.skills
                else:
                    profile['skills'] = []
            else:
                profile['skills'] = []

            if mentorProfile.status_list:
                if mentorProfile.status_list[0] != "":
                    profile['status'] = mentorProfile.status_list
                else:
                    profile['status'] = []
            else:
                profile['status'] = []
        
        self.write(json.dumps(list_profile))
