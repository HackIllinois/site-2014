import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from db import MobileConstants
from db.Sponsor import Sponsor
from db.Admin import Admin
from db.Skills import Skills
from db.NewsFeedItem import NewsFeedItem
from db.Schedule import Schedule
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

def construct_person_profile_for_json(person):
    person_json = {}

    return person_json

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

    if Attendee.search_database({'email_lower':email}).get():
            return Attendee.approvalStatus.status == "Rsvp Coming"
    elif Sponsor.search_database({'email_lower':email}).get():
        return True
    elif Admin.search_database({'email_lower':email}).get():
        return True
    else:
        return False

def get_hacker_data():
    """Sets the 'hacker_mobile' key in the memcache"""
    hackers = Attendee.query(Attendee.approvalStatus.status == "Rsvp Coming", ancestor=Attendee.get_default_event_parent_key())
    data = []
    for hackerProfile in hackers:
        name = ''
        if hackerProfile.nameFirst:
            name+=hackerProfile.nameFirst.strip().title() + ' '
        if hackerProfile.nameLast:
            name+=hackerProfile.nameLast.strip().title()
        profile = {'email':hackerProfile.email,
                    'school':hackerProfile.school.title(),
                    'year':hackerProfile.year,
                    'homebase':hackerProfile.homebase,
                    'fb_url':hackerProfile.pictureURL,
                    'database_key':hackerProfile.database_key,
                    'time':hackerProfile.updatedTime,
                    'mac_address':hackerProfile.mac_address,
                    'type':'hacker'}

        if hackerProfile.skills:
            if type(hackerProfile.skills) != type([]):
                logging.error("SKILLS: (type=%s) (userId=%s) %s" % (type(hackerProfile.skills), str(hackerProfile.userId), str(hackerProfile.skills)))
                hackerProfile.skills = [""]
                hackerProfile.put()
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

    return data

def get_staff_data():
    all_staff = Admin.search_database({})
    data = []

    for staff_profile in all_staff:
        profile = {'name':staff_profile.name.strip().title(),
                    'email':staff_profile.email,
                    'company':staff_profile.companyName,
                    'school':staff_profile.companyName,
                    'job_title':staff_profile.jobTitle,
                    'year':staff_profile.year,
                    'homebase':staff_profile.homebase,
                    'fb_url':staff_profile.pictureURL,
                    'database_key':staff_profile.database_key,
                    'time':staff_profile.updatedTime,
                    'mac_address':staff_profile.mac_address,
                    'type':'staff'}
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
        profile = {'name':mentor_profile.name.strip().title(),
                    'email':mentor_profile.email,
                    'company':mentor_profile.companyName,
                    'school':mentor_profile.companyName,
                    'job_title':mentor_profile.jobTitle,
                    'fb_url':mentor_profile.pictureURL,
                    'database_key':mentor_profile.database_key,
                    'homebase':mentor_profile.homebase,
                    'time':mentor_profile.updatedTime,
                    'mac_address':mentor_profile.mac_address,
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

        if mentor_profile.name != "":
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

        schedule_query = Schedule.search_database({})

        # Note: shitty hacky way to write this
        schedule_list_friday = []
        schedule_list_saturday = []
        schedule_list_sunday = []
        for schedule_item in schedule_query:
            item = {
                    'event_name':schedule_item.event_name,
                    'description':schedule_item.description,
                    'time':schedule_item.time + 18000, # 21600 is 6 hours in unix to compensate for time difference
                    'icon_url':schedule_item.icon_url,
                    'location':schedule_item.room_obj
            }
            if schedule_item.day == "Friday":
                schedule_list_friday.append(item)
            elif schedule_item.day == "Saturday":
                schedule_list_saturday.append(item)
            elif schedule_item.day == "Sunday":
                schedule_list_sunday.append(item)

        return self.write(json.dumps({'Friday':schedule_list_friday,'Saturday':schedule_list_saturday,'Sunday':schedule_list_sunday}))


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
    def get(self):
        valid_email = False
        if 'Email' in self.request.headers:
            valid_email = check_email_for_login(self.request.headers['Email'])

        if not valid_email:
            return self.write(json.dumps([]))

        newsFeed = NewsFeedItem.search_database({})
        newsFeedList = []
        for feedItem in newsFeed:
            item = {
                'description':feedItem.description,
                'time':feedItem.time,
                'icon_url':feedItem.icon_url,
                'emergency':feedItem.emergency,
                'announcement':feedItem.announcement,
                'hackillinois':feedItem.hackillinois,
            }

            if feedItem.highlighted:
                item['highlighted'] = feedItem.highlighted
            else:
                item['highlighted'] = []

            newsFeedList.append(item)


        return self.write(json.dumps(newsFeedList))


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

            allProfiles = get_people_memecache('all')

            for personProfile in allProfiles:
                if personProfile['database_key'] == int(keyParams):
                    return self.write(json.dumps([personProfile]))

        elif self.request.get('mac_address'):
            keyParams = self.request.get('mac_address')

            allProfiles = get_people_memecache('all')

            for personProfile in allProfiles:
                if personProfile['mac_address'] == keyParams:
                    return self.write(json.dumps([personProfile]))

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
            hackerProfile = Attendee.search_database({'email_lower':email}).get()
            staffProfile = Admin.search_database({'email_lower':email}).get()
            companyProfile = Sponsor.search_database({'email_lower':email}).get()

            if hackerProfile:
                # update datastore
                Attendee.update_search(updatedProfileDict, {'email_lower':email})

            elif staffProfile:
                # update datastore
                Admin.update_search(updatedProfileDict, {'email_lower':email})

            elif companyProfile:
                # update datastore
                Sponsor.update_search(updatedProfileDict, {'email_lower':email})

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
                    elif 'mac_address' in updatedKeys:
                        if isinstance(updatedProfileDict['mac_address'],str):
                            memcache_profile['mac_address'] = updatedProfileDict['mac_address']
                        else:
                            return self.write(json.dumps({'message':'Invalid mac_address'}))

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

            if skill.alias:
                if (skill.alias[0] != "") and (skill.alias[0] != " "):
                    skillDict['alias'] = skill.alias
                else:
                    skillDict['alias'] = []
            else:
                skillDict['alias'] = []

            if skill.tags:
                if (skill.tags[0] != "") and (skill.tags[0] != " "):
                    skillDict['tags'] = skill.tags
                else:
                    skillDict['tags'] = []
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
        hackerProfile = Attendee.search_database({'email_lower':email}).get()
        staffProfile = Admin.search_database({'email_lower':email}).get()
        mentorProfile = Sponsor.search_database({'email_lower':email}).get()

        list_profile = []

        if hackerProfile:
            name = ''
            if hackerProfile.nameFirst: name+=hackerProfile.nameFirst.strip().title() + ' '
            if hackerProfile.nameLast: name+=hackerProfile.nameLast.strip().title()
            profile = {'name':name,
            'email':hackerProfile.email,
            'school':hackerProfile.school.title(),
            'year':hackerProfile.year,
            'homebase':hackerProfile.homebase,
            'fb_url':hackerProfile.pictureURL,
            'database_key':hackerProfile.database_key ,
            'time':hackerProfile.updatedTime,
            'mac_address':hackerProfile.mac_address,
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
            profile = {'name':staffProfile.name.strip().title(),
            'email':staffProfile.email,
            'company':staffProfile.companyName,
            'school':staffProfile.companyName,
            'job_title':staffProfile.jobTitle,
            'year':staffProfile.year,
            'homebase':staffProfile.homebase,
            'fb_url':staffProfile.pictureURL,
            'database_key':staffProfile.database_key,
            'time':staffProfile.updatedTime,
            'mac_address':staffProfile.mac_address,
            'type':'staff'}

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
            profile = {'name':mentorProfile.name.strip().title(),
            'email':mentorProfile.email,
            'company':mentorProfile.companyName,
            'school':mentorProfile.companyName,
            'job_title':mentorProfile.jobTitle,
            'fb_url':mentorProfile.pictureURL,
            'homebase':mentorProfile.homebase,
            'database_key':mentorProfile.database_key ,
            'time':mentorProfile.updatedTime,
            'mac_address':mentorProfile.mac_address,
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

            list_profile.append(profile)

        self.write(json.dumps(list_profile))
