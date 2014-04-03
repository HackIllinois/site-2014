import MainAdminHandler
import urllib
from db.Attendee import Attendee
from db.Status import Status
from db import constants
from google.appengine.api import memcache
import logging
from datetime import datetime

class ApproveHandler(MainAdminHandler.BaseAdminHandler):
    def get(self, status=None, category=None, route=None):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        if status is not None:
            status = str(urllib.unquote(status))
            if status not in constants.APPROVE_STATUSES + ['a']:
                return self.abort(404, detail='Status <%s> does not exist.' % status)
        else:
            status = 'a'
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

        data['status_dropdown_text'] = 'Select a Status' if status is None or status == 'a' or status == 'b' or status == 'All' else status
        data['category_dropdown_text'] = 'Select a Category' if category is None else category if route is None else route

        if category is None:
            data['all_status_link'] = '/admin/approve'
        else:
            if route is None:
                data['all_status_link'] = '/admin/approve/a/'+category
            else:
                data['all_status_link'] = '/admin/approve/a/'+category+'/'+route

        if status is None:
            data['all_category_link'] = '/admin/approve'
        else:
            data['all_category_link'] = '/admin/approve/'+status

        data['all_status_link'] = urllib.quote(data['all_status_link'])
        data['all_category_link'] = urllib.quote(data['all_category_link'])

        data['statuses'] = []
        for s in constants.APPROVE_STATUSES:
            link = '/admin/approve/'+s
            if category:
                if route: link += '/'+category+'/'+route
                else: link += '/'+category
            data['statuses'].append({'text':s, 'link':urllib.quote(link)})

        data['categories'] = []
        for c in constants.CATEGORIES:
            link = '/admin/approve/'
            if status: link += status+'/'+c
            else: link += 'a/'+c
            data['categories'].append({'text':c, 'link':urllib.quote(link)})

        data['routes'] = []
        for r in constants.BUS_ROUTES:
            link = '/admin/approve/'
            if status: link += status+'/'+constants.TRAVEL_RIDE_BUS+'/'+r
            else: link += 'a/'+constants.TRAVEL_RIDE_BUS+'/'+r
            data['routes'].append({'text':r, 'link':urllib.quote(link)})


        # data['hackers'] = self.get_hackers_new_memcache(status, category, route, constants.USE_ADMIN_MEMCACHE)
        data['hackers'] = self.get_hackers_better_memcache(status, category, route)

        data['num_people'] = len(data['hackers'])

        data['approveCount'] = 0
        data['waitlistCount'] = 0
        data['notapproveCount'] = 0
        for h in data['hackers']:
            st = h['approvalStatus']['status']
            if st == 'Approved':
                data['approveCount'] += 1
            elif st == 'Waitlisted':
                data['waitlistCount'] += 1
            elif st == 'Not Approved':
                data['notapproveCount'] += 1

        return self.render("admin_approve.html", data=data, approveAccess=admin_user.approveAccess, mobileAccess=admin_user.mobileAccess, fullAccess=admin_user.fullAccess)


    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        userId = str(urllib.unquote(self.request.get('userId')))
        status = str(urllib.unquote(self.request.get('status')))

        db_user = Attendee.search_database({'userId':userId}).get()
        if not db_user:
            return self.abort(500, detail='User not in database')

        db_status = db_user.approvalStatus
        if db_status:
            if status == 'Approved':
                db_user.approvalStatus.approvedTime = datetime.now()
            elif status == 'Waitlisted':
                db_user.approvalStatus.waitlistedTime = datetime.now()
            db_user.approvalStatus.status = status
        else:
            if status == 'Approved':
                db_user.approvalStatus = Status(status=status, approvedTime=datetime.now())
            elif status == 'Waitlisted':
                db_user.approvalStatus = Status(status=status, waitlistedTime=datetime.now())
            else:
                db_user.approvalStatus = Status(status=status)

        db_user.put()

        return self.write('success')
