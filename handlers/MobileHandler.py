import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from google.appengine.api import users, memcache
import json

'''
    This is for the /mobile endpoint. All requests will pass through this and where the authentication check will be. Will be checking userId against all userId in the database.
   
    Note: Place userId in the header with key being AuthName
'''
class MobileLoginHandler:
    
    '''
       
        @return Reject request if the userId is not in the database otherwise let through
    '''
    def get(self):
        pass

    '''
        
        @return Reject request if the userId is not in the database otherwise let through
    '''
    def post(self):
        pass

'''
    
    
    Note:
'''
class ScheduleHandler:

    '''
        Get the current schedule of HackIllinois
        
        @return the schedule of HackIllinois
    '''
    def get(self):
        pass

    '''
        Update the schedule of HackIllinois
    
        @return Success or Fail (for now)
    '''
    def post(self):
        pass

'''
    
    Note:
'''
class MapsHandler:
    
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
        pass
    
    '''
        Updates a model for a location
       
        @return Success or Fail (for now)
    '''
    def post(self):
        pass

    '''
        Makes a new model for a location
        
        @return Success or Fail (for now)
    '''
    def put(self):
        pass

'''
    
    
    Note:
'''
class SupportTypeHandler:

    '''
       
        @return The list of Support Types
            for example:
                {
                    "General":[],
                    "Schedule":[],
                    "Rules":[]
                }
    '''
    def get(self):
        pass

    '''
        Update the support types of HackIllinois
       
        @return Success or Fail (for now)
    '''
    def post(self):
        pass

'''
    
    Note:
'''
class EmergencyHandler:

    '''
        
        
        @return Emergency Messages
    '''
    def get(self):
        pass

    '''
        Update an Emergency Message
        
        @return Success or Fail (for now)
    '''
    def post(self):
        pass

    '''
        Create a new Emergency Message
        
        Note: Must be an admin or current Staff
        
        @return Success or Fail (for now)
    '''
    def put(self):
        pass

'''
    
    Note:
'''
class NewsfeedHandler:

    '''
       
        @parameter before Top bound on the time for the NewsFeed
        @parameter since Bottom bound on the time for the NewsFeed (default should be your last time of the NewFeed card you have)
        @return The NewFeed models that are between the before and since parameters
    '''
    def get(self, before, since, count):
        pass

    '''
        Add an item to the news feed. Only Admin/Staff will be able to use this functionality.

        @return Success or fail (for now)
    '''
    def post(self):
        pass

'''
    
    Note:
'''
class StaffHandler:

    '''
       
        @return The models of all the Staff for HackIllinois
    '''
    def get(self):
        pass
    
    '''
        Update the current model associated with the userId
        
        @return Success or Fail (for now)
    '''
    def post(self):
        pass
    
    '''
        Create a new model for a Staff member for HackIllinois
       
        Note: Must be an admin or current Staff
       
        @return Success or Fail (for now)
    '''
    def put(self):
        pass

'''
    
    Note:
'''
class HackersHandler:

    '''
       
        @return The models of all the Hackers attendeeing HackIllinois
    '''
    def get(self):
        pass

    '''
        Update the current model associated with the userId
        
        @return Success or Fail (for now)
    '''
    def post(self):
        pass

    '''
        Create a new model for a Hacker that is attendeeing HackIllinois
        
        Note: Must be an admin or current Staff
        
        @return Success or Fail (for now)
    '''
    def put(self):
        pass

'''
    
    Note:
'''
class CompanyHandler:
    
    '''
        
        @return The models of all the Companies attendeeing HackIllinois
    '''
    def get(self):
        pass

    '''
        Update the current model associated with a company
        
        Note: Must be an admin or current Staff
       
        @return Success or Fail (for now)
    '''
    def post(self):
        pass

    '''
        Create a new model for a Company that is attendeeing HackIllinois
        
        Note: Must be an admin or current Staff
        
        @return
    '''
    def put(self):
        pass

'''
    
    Note:
'''
class SkillsHandler:
    
    '''
       
        @return A list of Skills that Hackers can have
    '''
    def get(self):
        pass

    '''
        Update the list of Skills Hackers can have
        
        @return
    '''
    def post(self):
        pass