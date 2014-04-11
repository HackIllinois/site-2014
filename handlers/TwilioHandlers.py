import MainHandler
from db import constants
from twilio.rest import TwilioRestClient

class TwilioHandler(MainHandler.Handler):
    client = None

    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.client = TwilioRestClient(constants.TWILIO_ACCOUNT_SID, constants.TWILIO_AUTH_TOKEN)

    def dispatch(self):
        super(TwilioHandler, self).dispatch()


class MassTextHandler(TwilioHandler):
    def get(self):
        message = self.client.sms.messages.create(
            body="Testing HackIllinois Twilio Number",
            to="+18479900616",
            from_="+17864225451"
        )

        self.write("Message with SID=%s was successfully sent!" % message.sid)

    def post(self):
        pass
