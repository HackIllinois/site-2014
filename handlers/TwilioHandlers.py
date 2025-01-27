import json
import urllib
import urllib2
import MainHandler
from db import constants
from db.PhoneNumber import PhoneNumber
import logging
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
import twilio.twiml


class TwilioHandler(MainHandler.Handler):
    client = None

    def dispatch(self):
        self.client = TwilioRestClient(constants.TWILIO_ACCOUNT_SID, constants.TWILIO_AUTH_TOKEN)
        super(TwilioHandler, self).dispatch()


class MassTextHandler(TwilioHandler):
    def post(self):
        from_number = self.request.get("From")
        if not from_number: self.abort(400, detail="No 'From' parameter given.")

        body = self.request.get("Body")
        if not body: self.abort(400, detail="No 'Body' parameter given.")

        q = PhoneNumber.search_database({"groups": "SendStaff"})
        authorized_senders = [i.number for i in q]

        if from_number in authorized_senders:
            q = PhoneNumber.search_database({"groups": "Staff"})
            group_numbers = [i.number for i in q]

            for number in group_numbers:
                message = self.client.sms.messages.create(
                    body=body,
                    to=number,
                    from_="+17864225451"
                )
            logging.info("%s sent a message to the group: %s" % (from_number, body))
        else:
            # TODO: Change to send email to support@hackillinois.org
            message = self.client.sms.messages.create(
                body="You are not authorized to send messages to this number.",
                to=from_number,
                from_="+17864225451"
            )
            logging.info("Unauthorized user tried to send a message: %s" % from_number)


class TextEveryoneHandler(TwilioHandler):
    def post(self):
        from_number = self.request.get("From")
        if not from_number: self.abort(400, detail="No 'From' parameter given.")

        body = self.request.get("Body")
        if not body: self.abort(400, detail="No 'Body' parameter given.")

        q = PhoneNumber.search_database({"groups": "SendStaff"})
        authorized_senders = [i.number for i in q]

        if from_number in authorized_senders:
            data = {
                'sms_body': body
            }

            req = urllib2.Request('http://23.236.61.209:5000/send', data=urllib.urlencode(data))
            resp = urllib2.urlopen(req)
            content = resp.read()

            logging.info("%s sent a message to everyone with body: %s" % (from_number, body))
        else:
            # TODO: Change to send email to support@hackillinois.org
            try:
                message = self.client.sms.messages.create(
                    body="You are not authorized to send messages to this number.",
                    to=from_number,
                    from_="+17864225451"
                )
            except TwilioRestException, e:
                print 'rest exception: %s' % e

            logging.info("Unauthorized user tried to send a message: %s" % from_number)


class AllNumbersHandler(MainHandler.Handler):
    def get(self):
        q = PhoneNumber.search_database({"groups": "Staff"})
        group_numbers = [i.number for i in q]

        numbers_to_show = []

        # Send to all staff
        for number in group_numbers:
            numbers_to_show.append(number)

        # Send to all Attendees
        for number in constants.ATTENDEE_NUMBERS:
            numbers_to_show.append(number)

        out = {
            'phone_numbers': numbers_to_show
        }

        self.write(json.dumps(out))
