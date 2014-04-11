import MainHandler
from db import constants
from google.appengine.api import users
from db.Attendee import Attendee
import hashlib

FIRST_SURVEY_URL = "https://uiuc.qualtrics.com/SE/?SID=SV_9o8VsW4h7QRpUBn&uid={0}"
SECOND_SURVEY_URL = "https://survey.az1.qualtrics.com/SE/?SID=SV_56B6x4cmftCrGwB&uid={0}"

def get_uid():
    user = users.get_current_user()
    if not user:
        return None
    hackers = Attendee.query(Attendee.isRegistered == True,
                             Attendee.userId == user.user_id(),
                             Attendee.approvalStatus.status == 'Rsvp Coming',
                             ancestor=Attendee.get_default_event_parent_key())
    if hackers.count() == 0:
        return None
    email = user.email()
    return hashlib.sha256(email + constants.RESEARCH_PEPPER).hexdigest()

class ResearchHandler(MainHandler.Handler):
    def get(self):
        uid = get_uid()
        if not uid:
            self.redirect("/")
        else:
            self.render("research.html", uid=uid)

class ResearchRedirect(MainHandler.Handler):
    def get(self, form):
        uid = get_uid()
        if not uid:
            self.error(403)
        if form == "1":
            self.redirect(FIRST_SURVEY_URL.format(uid))
        elif form == "2":
            self.redirect(SECOND_SURVEY_URL.format(uid))
        else:
            self.error(404)

class ResearchComplete(MainHandler.Handler):
    def get(self):
        self.render("research_thanks.html")
