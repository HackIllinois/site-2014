import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db.Status import Status
from db import constants
from google.appengine.api import memcache
import logging
from datetime import datetime
import json

class AllHackersHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, status=None, category=None, route=None):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        if status is not None:
            status = str(urllib.unquote(status))
            if status not in constants.STATUSES + ['c']:
                return self.abort(404, detail='Status <%s> does not exist.' % status)
        else:
            status = 'c'
        if category is not None:
            category = str(urllib.unquote(category))
            if category not in constants.CATEGORIES:
                return self.abort(404, detail='Category <%s> does not exist.' % category)
        if route is not None:
            route = str(urllib.unquote(route))
            if category != constants.TRAVEL_RIDE_BUS:
                return self.abort(404, detail='Incorrect category <%s>.' % category)
            if route not in constants.BUS_ROUTES:
                return self.abort(404, detail='Route <%s> does not exist.' % route)

        data = {}

        if status is None:
            data['export_url'] = '/admin/export'
        elif category is None:
            data['export_url'] = '/admin/export/' + status
        elif route is None:
            data['export_url'] = '/admin/export/' + status + '/' + category
        else:
            data['export_url'] = '/admin/export/' + status + '/' + category + '/' + route

        data['status_dropdown_text'] = 'Select a Status' if status is None or status == 'a' or status == 'b' or status == 'c' or status == 'All' else status
        data['category_dropdown_text'] = 'Select a Category' if category is None else category if route is None else route

        if category is None:
            data['all_status_link'] = '/admin/allhackers'
        else:
            if route is None:
                data['all_status_link'] = '/admin/allhackers/c/'+category
            else:
                data['all_status_link'] = '/admin/allhackers/c/'+category+'/'+route

        if status is None or status == 'c':
            data['all_category_link'] = '/admin/allhackers'
        else:
            data['all_category_link'] = '/admin/allhackers/'+status

        data['all_status_link'] = urllib.quote(data['all_status_link'])
        data['all_category_link'] = urllib.quote(data['all_category_link'])

        data['statuses'] = []
        for s in constants.STATUSES:
            link = '/admin/allhackers/'+s
            if category:
                if route: link += '/'+category+'/'+route
                else: link += '/'+category
            data['statuses'].append({'text':s, 'link':urllib.quote(link)})

        data['categories'] = []
        for c in constants.CATEGORIES:
            link = '/admin/allhackers/'
            if status: link += status+'/'+c
            else: link += 'c/'+c
            data['categories'].append({'text':c, 'link':urllib.quote(link)})

        data['routes'] = []
        for r in constants.BUS_ROUTES:
            link = '/admin/allhackers/'
            if status: link += status+'/'+constants.TRAVEL_RIDE_BUS+'/'+r
            else: link += 'c/'+constants.TRAVEL_RIDE_BUS+'/'+r
            data['routes'].append({'text':r, 'link':urllib.quote(link)})

        # data['hackers'] = self.get_hackers_new_memcache(status, category, route, constants.USE_ADMIN_MEMCACHE)
        data['hackers'] = self.get_hackers_better_memcache(status, category, route)

        data['num_people'] = len(data['hackers'])

        return self.render("admin_all_hackers.html", data=data, access=json.loads(admin_user.access))
