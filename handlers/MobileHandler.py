import MainHandler
import urllib, logging, re
from db.Attendee import Attendee
from db import constants
from google.appengine.api import users, memcache
import json

'''
    
    
    Note:
'''
class ScheduleHandler(MainHandler.BaseMobileHandler):

    '''
        Get the current schedule of HackIllinois
        
        @return the schedule of HackIllinois
    '''
    def get(self):
        return self.write(json.dumps({'Schedule':[]}))

    '''
        Update the schedule of HackIllinois
    
        @return Success or Fail (for now)
    '''
#    def post(self):
#        pass
#
#    def put(self):
#        pass
#
#    def delete(self):
#        pass

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
        Updates a model for a location
       
        @return Success or Fail (for now)
    '''
#    def post(self):
#        pass
#
#    '''
#        Makes a new model for a location
#        
#        @return Success or Fail (for now)
#    '''
#    def put(self):
#        pass

#    def delete(self):
#        pass

'''
    
    
    Note:
'''
class SupportTypeHandler(MainHandler.BaseMobileHandler):

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
        return self.write(json.dumps({'General':['general1'],'Schedule':['schedule1','schedule2','schedule3'],'Rules':['rule1','rule2']}))

    '''
        Update the support types of HackIllinois
       
        @return Success or Fail (for now)
    '''
#    def post(self):
#        pass
#
#    def put(self):
#        pass
#
#    def delete(self):
#        pass

'''
    
    Note:
'''
class EmergencyHandler(MainHandler.BaseMobileHandler):

    '''
        
        
        @return Emergency Messages
    '''
    def get(self):
        return self.write(json.dumps({'Emergency':[]}))

    '''
        Update an Emergency Message
        
        @return Success or Fail (for now)
    '''
#    def post(self):
#        pass
#
#    '''
#        Create a new Emergency Message
#        
#        Note: Must be an admin or current Staff
#        
#        @return Success or Fail (for now)
#    '''
#    def put(self):
#        pass

#    def delete(self):
#        pass

'''
    
    Note:
'''
class NewsfeedHandler(MainHandler.BaseMobileHandler):

    '''
       
        @parameter before Top bound on the time for the NewsFeed
        @parameter since Bottom bound on the time for the NewsFeed (default should be your last time of the NewFeed card you have)
        @return The NewFeed models that are between the before and since parameters
    '''
    def get(self):
        return self.write(json.dumps({'NewsFeed':[]}))

    '''
        Add an item to the news feed. Only Admin/Staff will be able to use this functionality.

        @return Success or fail (for now)
    '''
#    def post(self):
#        pass
#
#    def put(self):
#        pass
#
#    def delete(self):
#        pass

'''
    
    Note:
'''
class StaffHandler(MainHandler.BaseMobileHandler):

    '''
       
        @return The models of all the Staff for HackIllinois
    '''
    def get(self):
        return self.write(json.dumps({'Staff':[]}))

    '''
        Update the current model associated with the userId
        
        @return Success or Fail (for now)
    '''
#    def post(self):
#        pass
#    
#    '''
#        Create a new model for a Staff member for HackIllinois
#       
#        Note: Must be an admin or current Staff
#       
#        @return Success or Fail (for now)
#    '''
#    def put(self):
#        pass
#
#    def delete(self):
#        pass

'''
    
    Note:
'''
class HackersHandler(MainHandler.BaseMobileHandler):

    '''
       
        @return The models of all the Hackers attendeeing HackIllinois
    '''
    def get(self):
        return self.write(json.dumps({'Hacker':[]}))

    '''
        Update the current model associated with the userId
        
        @return Success or Fail (for now)
    '''
#    def post(self):
#        pass
#
#    '''
#        Create a new model for a Hacker that is attendeeing HackIllinois
#        
#        Note: Must be an admin or current Staff
#        
#        @return Success or Fail (for now)
#    '''
#    def put(self):
#        pass
#
#    def delete(self):
#        pass

'''
    
    Note:
'''
class CompanyHandler(MainHandler.BaseMobileHandler):
    
    '''
        
        @return The models of all the Companies attendeeing HackIllinois
    '''
    def get(self):
        return self.write(json.dumps({'Company':[]}))

    '''
        Update the current model associated with a company
        
        Note: Must be an admin or current Staff
       
        @return Success or Fail (for now)
    '''
#    def post(self):
#        pass
#
#    '''
#        Create a new model for a Company that is attendeeing HackIllinois
#        
#        Note: Must be an admin or current Staff
#        
#        @return
#    '''
#    def put(self):
#        pass
#
#    def delete(self):
#        pass

'''
    
    Note:
'''
class SkillsHandler(MainHandler.BaseMobileHandler):
    
    '''
       
        @return A list of Skills that Hackers can have
    '''
    def get(self):
        return self.write(json.dumps({'Skills':['skill1','skill2','skill3','skill4','skill5']}))

    '''
        Update the list of Skills Hackers can have
        
        @return
    '''
#    def post(self):
#        pass
#
#    def put(self):
#        pass
#
#    def delete(self):
#        pass
