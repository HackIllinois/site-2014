import MainHandler
import logging

from tropo import Session, Tropo

from google.appengine.api import mail


class TropoHandler(MainHandler.Handler):

    """ Handle an incoming call or text to our phone number (312-757-5638)
    This is handled by Tropo (http://www.tropo.com)"""

    def post(self):
        session = Session(self.request.body)
        t = Tropo()

        if session.fromaddress['channel'] == 'VOICE':
            self.handleVoiceCall(session, t)
        else:
            self.handleSms(session, t)

        json = t.RenderJson()
        logging.info("Json reuslt: %s" % json)
        self.write(json)

    def handleVoiceCall(self, session, t):
        """ Handle an incoming voice call. """
        t.say("Welcome to HackIllinois! Please wait while we try to connect your call.")
        # Just transfer the call to Matthew for now. If anyone actually uses
        # this we'll change it for later
        t.transfer("+12819001868")

    def handleSms(self, session, t):
        """ Handle an incoming text """
        t.say("Your message has been passed along to HackIllinois staff!")

        text_body = """SMS Received from %s
Note that you cannot reply to this email -- You'll have to actually text them back. If you'd like to code that feature you're welcome to! ;)
=============

%s""" % (session.fromaddress['id'], session.initialText)

        mail.send_mail(sender="matthew@hackillinois.org",
                       to="contact@hackillinois.org",
                       subject="SMS Received from %s" % session.fromaddress['id'],
                       body=text_body)
