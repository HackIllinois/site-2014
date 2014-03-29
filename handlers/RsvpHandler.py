import urllib
import logging
import re
import json
from datetime import datetime

import MainHandler

from db.Attendee import Attendee
from db.Resume import Resume
from db.Status import Status
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class RsvpHandler(MainHandler.Handler):
    def get(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')

        db_user = Attendee.search_database({'userId': user.user_id()}).get()

        if db_user is None:
            return self.redirect('/apply/closed')

        if db_user.isRegistered == False:
            return self.redirect('/apply/closed')

        if db_user.approvalStatus is None:
            return self.redirect('/rsvp/pending')

        if db_user.approvalStatus.status is 'Rsvp Not Coming':
            return self.redirect('/rsvp/no')

        if db_user.approvalStatus.status is 'No Rsvp':
            return self.redirect('/rsvp/closed')

        if db_user.approvalStatus.status == 'Rsvp Not Coming':
            return self.redirect('/rsvp/no')

        if db_user.approvalStatus.status not in ['Awaiting Response', 'Rsvp Coming']:
            return self.redirect('/rsvp/pending')

        data = {}
        data['title'] = constants.RSVP_TITLE
        data['errors'] = {} # Needed for template to render

        data['username'] = db_user.userNickname
        data['email'] = db_user.email

        data['status'] = db_user.approvalStatus.status

        lists = {
            'micro1':constants.MICRO1, 'micro2':constants.MICRO2
            }

        for l, options in lists.iteritems(): data[l] = [ {'name':n[0], 'checked':False, 'link':n[1]} for n in options]

        data['labEquipment'] = [ {'name':n, 'checked':False} for n in constants.LABEQUIPMENT]

        data['travelArrangements'] = [ {'name':n, 'checked':False} for n in constants.TRAVEL_ARRANGEMENTS ]

        data['busRoutes'] = [ {'name':n, 'selected':False} for n in constants.BUS_ROUTES ]

        choose_one_fields = {
            'travel':('travelArrangements','checked'), 'busRoute':('busRoutes','selected')
            }

        for field, conn in choose_one_fields.iteritems():
            value = getattr(db_user, field)
            if value:
                for i in data[conn[0]]:
                    if i['name'] == value:
                        i[conn[1]] = True
                        break

        # Multi-choice check box
        choose_multiple_fields = {
            'micro1':('micro1','checked'), 'micro2':('micro2','checked'), 'labEquipment':('labEquipment','checked')
            }

        for field, conn in choose_multiple_fields.iteritems():
            value = getattr(db_user, field)
            if value:
                for i in data[conn[0]]:
                    if i['name'] in value:
                        i[conn[1]] = True

        data['logoutUrl'] = users.create_logout_url('/apply')

        self.render("rsvp.html", data=data)

    def post(self):
        user = users.get_current_user()
        if not user: return self.abort(500, detail='User not logged in')

        db_user = Attendee.search_database({'userId':user.user_id()}).get()

        if db_user is None:
            return self.redirect('/apply/closed')

        if db_user.isRegistered == False:
            return self.redirect('/apply/closed')

        if db_user.approvalStatus is None:
            return self.redirect('/rsvp/pending')

        if db_user.approvalStatus.status is 'Rsvp Not Coming':
            return self.redirect('/rsvp/no')

        if db_user.approvalStatus.status is 'No Rsvp':
            return self.redirect('/rsvp/closed')

        if db_user.approvalStatus.status == 'Rsvp Not Coming':
            return self.redirect('/rsvp/no')

        if db_user.approvalStatus.status not in ['Awaiting Response', 'Rsvp Coming']:
            return self.redirect('/rsvp/pending')

        # Initialization
        x = {}
        errors = {} # Note: 1 error per field
        valid = True

        isAttending = self.request.get("attend")
        if isAttending not in ["Yes", "No"]:
            errors['attending'] = "Invalid Bus Route"
            valid = False

        elif isAttending == "Yes":
            x['approvalStatus'] = Status(rsvpTime=datetime.now(),
                                         waitlistedTime=db_user.approvalStatus.waitlistedTime,
                                         approvedTime=db_user.approvalStatus.approvedTime,
                                         emailedTime=db_user.approvalStatus.emailedTime,
                                         status = 'Rsvp Coming')

            categories = ['micro1', 'micro2', 'labEquipment']
            for category in categories:
                l = self.request.get_all(category)
                x[category] = ','.join(l)


            x['travel'] = self.request.get('travel')
            if x['travel'] == 'I would like to ride a HackIllinois bus':
                x['busRoute'] = self.request.get('busRoute')
            else:
                x['busRoute'] = None

            # ---------- BEGIN VALIDATION ----------
            for m1 in x['micro1'].split(','):
                micro1Flag = True
                for temp in constants.MICRO1:
                    if temp[0] == m1 or not m1:
                        micro1Flag = False
                if micro1Flag:
                    errors['micro1'] = "Invalid Microcontrollers"
                    valid = False
                    break

            for m2 in x['micro2'].split(','):
                micro2Flag = True
                for temp in constants.MICRO2:
                    if temp[0] == m2 or not m2:
                        micro2Flag = False
                if micro2Flag:
                    errors['micro2'] = "Invalid Microcontrollers"
                    valid = False
                    break


            for l in x['labEquipment'].split(','):
                if l not in constants.LABEQUIPMENT and l:
                    errors['labEquipment'] = "Invalid Lab Equipment"
                    valid = False
                    break

            if not x['travel'] or x['travel'] == constants.TRAVEL_NO_RESPONSE:
               errors['travel'] = "Provide Travel Plans"
               valid = False

            if not x['travel'] and (x['travel'] not in constants.TRAVEL_ARRANGEMENTS):
               errors['travel'] = "Invalid Travel Plans"
               valid = False

            if x['travel'] == constants.TRAVEL_RIDE_BUS:
                if 'busRoute' not in x or not x['busRoute'] or x['busRoute'] not in constants.BUS_ROUTES:
                    errors['busRoute'] = "Invalid Bus Route"
                    valid = False

            # ---------- END VALIDATION ----------

        else:
            x['approvalStatus'] = Status(rsvpTime=datetime.now(),
                                         waitlistedTime=db_user.approvalStatus.waitlistedTime,
                                         approvedTime=db_user.approvalStatus.approvedTime,
                                         emailedTime=db_user.approvalStatus.emailedTime,
                                         status = 'Rsvp Not Coming')

        if valid:
            Attendee.update_search(x, {'userId':user.user_id()})
            if isAttending == "Yes":
                return self.redirect("/rsvp/yes")
            else:
                return self.redirect("/rsvp/no")
        else:
            print
            print errors
            print
            return self.redirect("/apply/rsvp")

class RsvpYesHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header=constants.RSVP_YES_HEADER,
                            message=constants.RSVP_YES_MESSAGE,
                            showSocial=True )

class RsvpNoHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header=constants.RSVP_NO_HEADER,
                            message=constants.RSVP_NO_MESSAGE,
                            showSocial=True )

class NotApprovedHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header=constants.NOT_APPROVED_HEADER,
                            message=constants.NOT_APPROVED_MESSAGE,
                            showSocial=True )

class RsvpClosedHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header=constants.RSVP_CLOSED_HEADER,
                            message=constants.RSVP_CLOSED_MESSAGE,
                            showSocial=True )
