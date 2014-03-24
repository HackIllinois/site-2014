import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db import constants
from google.appengine.api import memcache
import logging

class ApproveBaseHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        data = {}
        data['num_people'] = 10
        data['dropdown_button_text'] = 'Select a Category'
        data['categories'] = [{'text':constants.TRAVEL_PROVIDE_OWN_TRANSIT, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_PROVIDE_OWN_TRANSIT_URL)},
                              {'text':constants.TRAVEL_ALREADY_AT_UIUC, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_ALREADY_AT_UIUC_URL)},
                              {'text':constants.TRAVEL_NO_RESPONSE, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_NO_RESPONSE_URL)}]
        data['routes'] = [ {'text':r, 'link':urllib.quote('/admin/approve/bus/'+r)} for r in constants.BUS_ROUTES ]

        return self.render("admin_approve_base.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)

class ApproveRouteHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, route):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        route = str(urllib.unquote(route))

        if route not in constants.BUS_ROUTES:
            return self.abort(404, detail='Route <%s> does not exist.' % route)

        data = {}
        data['dropdown_button_text'] = route
        data['categories'] = [{'text':constants.TRAVEL_PROVIDE_OWN_TRANSIT, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_PROVIDE_OWN_TRANSIT_URL)},
                              {'text':constants.TRAVEL_ALREADY_AT_UIUC, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_ALREADY_AT_UIUC_URL)},
                              {'text':constants.TRAVEL_NO_RESPONSE, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_NO_RESPONSE_URL)}]
        data['routes'] = [ {'text':r, 'link':urllib.quote('/admin/approve/bus/'+r)} for r in constants.BUS_ROUTES ]

        data['hackers'] = self.get_route_memecache(route, constants.USE_ADMIN_MEMCACHE)

        data['num_people'] = len(data['hackers'])

        return self.render("admin_approve_table.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)

    def get_route_memecache(self, route, use_memcache=False):
        """Gets the 'routes/<route>' key from memcache"""
        route_hackers = memcache.get('routes/' + route)
        if route_hackers is None or not use_memcache:
            route_hackers = self.set_route_memecache(route)
        return route_hackers

    def set_route_memecache(self, route):
        """Sets the 'routes/<route>' key in memcache"""
        q = Attendee.search_database({'isRegistered':True, 'busRoute':route})
        data = []
        for hacker in q:
            data.append({ 'nameFirst':hacker.nameFirst,
                          'nameLast':hacker.nameLast,
                          'email':hacker.email,
                          'gender':hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                          'school':hacker.school,
                          'year':hacker.year,
                          'linkedin':hacker.linkedin,
                          'github':hacker.github,
                          'shirt':hacker.shirt,
                          'food':'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                          'projectType':hacker.projectType,
                          'resume':hacker.resume,
                          'registrationTime':hacker.registrationTime.strftime('%x %X'),
                          'isApproved':hacker.isApproved,
                          'userId':hacker.userId})

        if not memcache.add('routes/' + route, data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return data

class ApproveCategoryHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, category):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        category = str(urllib.unquote(category))

        if category not in [constants.TRAVEL_PROVIDE_OWN_TRANSIT_URL, constants.TRAVEL_ALREADY_AT_UIUC_URL, constants.TRAVEL_NO_RESPONSE_URL]:
            return self.abort(404, detail='Category <%s> does not exist.' % category)

        data = {}
        data['dropdown_button_text'] = ''
        if category == constants.TRAVEL_PROVIDE_OWN_TRANSIT_URL:
            data['dropdown_button_text'] = constants.TRAVEL_PROVIDE_OWN_TRANSIT
        elif category == constants.TRAVEL_ALREADY_AT_UIUC_URL:
            data['dropdown_button_text'] = constants.TRAVEL_ALREADY_AT_UIUC
        elif category == constants.TRAVEL_NO_RESPONSE_URL:
            data['dropdown_button_text'] = constants.TRAVEL_NO_RESPONSE

        data['categories'] = [{'text':constants.TRAVEL_PROVIDE_OWN_TRANSIT, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_PROVIDE_OWN_TRANSIT_URL)},
                              {'text':constants.TRAVEL_ALREADY_AT_UIUC, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_ALREADY_AT_UIUC_URL)},
                              {'text':constants.TRAVEL_NO_RESPONSE, 'link':urllib.quote('/admin/approve/'+constants.TRAVEL_NO_RESPONSE_URL)}]
        data['routes'] = [ {'text':r, 'link':urllib.quote('/admin/approve/bus/'+r)} for r in constants.BUS_ROUTES ]

        data['hackers'] = self.get_category_memecache(category, constants.USE_ADMIN_MEMCACHE)

        data['num_people'] = len(data['hackers'])

        return self.render("admin_approve_table.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)

    def get_category_memecache(self, category, use_memcache=False):
        """Gets the 'categories/<category>' key from memcache"""
        category_hackers = memcache.get('categories/' + category)
        if category_hackers is None or not use_memcache:
            category_hackers = self.set_category_memecache(category)
        return category_hackers


    def set_category_memecache(self, category):
        """Sets the 'categories/<category>' key in memcache"""
        q = None

        if category == constants.TRAVEL_PROVIDE_OWN_TRANSIT_URL:
            q = Attendee.search_database({'isRegistered':True, 'travel':constants.TRAVEL_PROVIDE_OWN_TRANSIT})
        elif category == constants.TRAVEL_ALREADY_AT_UIUC_URL:
            q = Attendee.search_database({'isRegistered':True, 'travel':constants.TRAVEL_ALREADY_AT_UIUC})
        elif category == constants.TRAVEL_NO_RESPONSE_URL:
            q = Attendee.search_database({'isRegistered':True})
            q = q.filter(Attendee.travel.IN([None, '']))

        if q is None:
            # Shouldn't happen: sanity check
            return None

        data = []
        for hacker in q:
            data.append({ 'nameFirst':hacker.nameFirst,
                          'nameLast':hacker.nameLast,
                          'email':hacker.email,
                          'gender':hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                          'school':hacker.school,
                          'year':hacker.year,
                          'linkedin':hacker.linkedin,
                          'github':hacker.github,
                          'shirt':hacker.shirt,
                          'food':'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                          'projectType':hacker.projectType,
                          'resume':hacker.resume,
                          'registrationTime':hacker.registrationTime.strftime('%x %X'),
                          'isApproved':hacker.isApproved,
                          'userId':hacker.userId})

        if not memcache.add('categories/' + category, data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return data
