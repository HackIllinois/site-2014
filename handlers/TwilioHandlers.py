import MainHandler
from db import constants
import logging
from twilio.rest import TwilioRestClient
import twilio.twiml

class TwilioHandler(MainHandler.Handler):
    client = None

    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.client = TwilioRestClient(constants.TWILIO_ACCOUNT_SID, constants.TWILIO_AUTH_TOKEN)

    def dispatch(self):
        super(TwilioHandler, self).dispatch()


class MassTextHandler(TwilioHandler):
    group_numbers = [
        "+12819001868",
        "+18159017433",
        "+12177024289",
        "+18472208144",
        "+12245950714",
        "+16183634733",
        "+16307300483",
        "+18478990864",
        "+12014217556",
        "+12164017524",
        "+18477698729",
        "+18474716440",
        "+13148826802",
        "+18479900616",
        "+14109177282",
        "+12178190512",
        "+15089250150",
        "+16507841346",
        "+16302153819",
        "+19082942804",
        "+18153252310",
        "+16309950526",
        "+12178190184",
        "+13017048566",
        "+18153252310",
        "+16308530925"
    ]

    group_number = ['+16306390298','+18479900616','+17082090324']

    authorised_msgrs = {
        "+16306390298" : "Austin",
        "+12819001868": "Matthew",
        "+17736095477": "Emily"
    }
    def post(self):
        from_number = self.request.get("From")
        if from_number and from_number in authorised_msgrs:
            body = self.request.get("Body")
            for number in group_number:
                message = self.client.sms.messages.create(
                    body=body,
                    to=number,
                    from_="+17864225451"
                )
            logging.info("%s sent a message to the group" % (authorised_msgrs[from_number]))
        else:
            resp = twilio.twiml.Response().message("Eat Shit and Die.")
            logging.info("Someone ate shit and died.")

    def get(self):
        pass
