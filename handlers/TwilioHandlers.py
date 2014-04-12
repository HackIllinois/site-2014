import MainHandler
from db import constants
from db.PhoneNumber import PhoneNumber
import logging
from twilio.rest import TwilioRestClient
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
        authorized_senders = [ i.number for i in q ]

        if from_number in authorized_senders:
            q = PhoneNumber.search_database({"groups": "Staff"})
            group_numbers = [ i.number for i in q ]

            for number in group_numbers:
                message = self.client.sms.messages.create(
                    body=body,
                    to=number,
                    from_="+17864225451"
                )
            logging.info("%s sent a message to the group: %s" % (authorized_senders[from_number], body))
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
        authorized_senders = [ i.number for i in q ]

        if from_number in authorized_senders:
            q = PhoneNumber.search_database({"groups": "Staff"})
            group_numbers = [ i.number for i in q ]

            # Send to all staff
            for number in group_numbers:
                message = self.client.sms.messages.create(
                    body=body,
                    to=number,
                    from_="+17077223706"
                )

            # Send to all Attendees
            for number in constants.ATTENDEE_NUMBERS:
                message = self.client.sms.messages.create(
                    body=body,
                    to=number,
                    from_="+17077223706"
                )

            logging.info("%s sent a message to the group: %s" % (authorized_senders[from_number], body))
        else:
            # TODO: Change to send email to support@hackillinois.org
            message = self.client.sms.messages.create(
                body="You are not authorized to send messages to this number.",
                to=from_number,
                from_="+17864225451"
            )
            logging.info("Unauthorized user tried to send a message: %s" % from_number)
