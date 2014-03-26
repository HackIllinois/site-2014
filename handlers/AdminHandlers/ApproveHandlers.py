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
            if status not in constants.STATUSES + ['All']:
                return self.abort(404, detail='Status <%s> does not exist.' % status)
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

        data['status_dropdown_text'] = 'Select a Status' if status is None else status
        data['category_dropdown_text'] = 'Select a Category' if category is None else category if route is None else route

        if category is None:
            data['all_status_link'] = '/admin/approve'
        else:
            if route is None:
                data['all_status_link'] = '/admin/approve/All/'+category
            else:
                data['all_status_link'] = '/admin/approve/All/'+category+'/'+route

        if status is None:
            data['all_category_link'] = '/admin/approve'
        else:
            data['all_category_link'] = '/admin/approve/'+status

        data['all_status_link'] = urllib.quote(data['all_status_link'])
        data['all_category_link'] = urllib.quote(data['all_category_link'])

        data['statuses'] = []
        for s in constants.STATUSES:
            link = '/admin/approve/'+s
            if category:
                if route: link += '/'+category+'/'+route
                else: link += '/'+category
            data['statuses'].append({'text':s, 'link':urllib.quote(link)})

        data['categories'] = []
        for c in constants.CATEGORIES:
            link = '/admin/approve/'
            if status: link += status+'/'+c
            else: link += 'All/'+c
            data['categories'].append({'text':c, 'link':urllib.quote(link)})

        data['routes'] = []
        for r in constants.BUS_ROUTES:
            link = '/admin/approve/'
            if status: link += status+'/'+constants.TRAVEL_RIDE_BUS+'/'+r
            else: link += 'All/'+constants.TRAVEL_RIDE_BUS+'/'+r
            data['routes'].append({'text':r, 'link':urllib.quote(link)})


        data['hackers'] = self.get_hackers_new_memecache(status, category, route, constants.USE_ADMIN_MEMCACHE)

        data['num_people'] = len(data['hackers'])

        return self.render("admin_approve.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)


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

        # Delete memcache key so /admin/approve is updated
        # memcache.delete('hackers')

        return self.write('success')


    def get_hackers_new_memecache(self, status=None, category=None, route=None, use_memcache=False):
        """Gets the 'hackers/<status>/<category>/<route>' key from the memcache and updates the memcache if the key is not in the memcache"""
        if use_memcache:
            key = 'hackers/' + str(status) + '/' + str(category) + '/' + str(route)
            data = memcache.get(key)
            if data is None: data = self.set_hackers_new_memcache(status, category, route)
            return data
        else:
            return self.set_hackers_new_memcache(status, category, route)


    def set_hackers_new_memcache(self, status=None, category=None, route=None):
        """Sets the 'hackers/<status>/<category>/<route>' key in the memcache"""
        key = 'hackers/' + str(status) + '/' + str(category) + '/' + str(route)
        hackers = None

        # Change search of category='I have not responded to this quesiton' to ''
        category = '' if category == 'I have not responded to this quesiton' else category

        if status is not None and status != 'All':
            if category is not None:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status, Attendee.travel == category, Attendee.busRoute == route, ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status, Attendee.travel == category, ancestor=Attendee.get_default_event_parent_key())
            else:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status, Attendee.busRoute == route, ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.approvalStatus.status == status, ancestor=Attendee.get_default_event_parent_key())
        else:
            if category is not None:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.travel == category, Attendee.busRoute == route, ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.travel == category, ancestor=Attendee.get_default_event_parent_key())
            else:
                if route is not None:
                    hackers = Attendee.query(Attendee.isRegistered == True, Attendee.busRoute == route, ancestor=Attendee.get_default_event_parent_key())
                else:
                    hackers = Attendee.query(Attendee.isRegistered == True, ancestor=Attendee.get_default_event_parent_key())

        data = []
        for hacker in hackers:
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
                          'userId':hacker.userId,
                          'travel':hacker.travel,
                          'busRoute':hacker.busRoute,
                          'approvalStatus':{'status':hacker.approvalStatus.status,
                                            'approvedTime':hacker.approvalStatus.approvedTime.strftime('%x %X') if hacker.approvalStatus.approvedTime else None,
                                            'waitlistedTime':hacker.approvalStatus.waitlistedTime.strftime('%x %X') if hacker.approvalStatus.waitlistedTime else None,
                                            'rsvpTime':hacker.approvalStatus.rsvpTime.strftime('%x %X') if hacker.approvalStatus.rsvpTime else None} if hacker.approvalStatus else None,
                          'groupNumber':hacker.groupNumber })

        if not memcache.add(key, data, time=constants.MEMCACHE_TIMEOUT):
            logging.error('Memcache set failed.')

        return data
