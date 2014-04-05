import MainAdminHandler
from db import constants
from db.Attendee import Attendee
import re
import urllib
from datetime import datetime
import json


class CheckNoReplyHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.require_and_get_admin_user()

        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to email attendees.')

        data = {}
        return self.render('admin_check_no_reply.html', data=data, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.require_and_get_admin_user()

        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to email attendees.')

        orig_str = str(urllib.unquote(self.request.get('emails')))
        email_str = orig_str.strip()
        if not email_str:
            return self.write("Error: No emails entered.")

        # Split emails by comma, semicolon, space, or newline (or some combination of all of those)
        emails = re.split(r'[,; \n]', email_str)

        for i in xrange(len(emails)):
            emails[i] = emails[i].strip()

        valid_emails = []
        invalid_emails = []
        for email in emails:
            if re.match(constants.EMAIL_MATCH, email):
                valid_emails.append(email)
            else:
                invalid_emails.append(email)

        hackers = Attendee.query(Attendee.email.IN(valid_emails))

        for person in hackers:
            if person.approvalStatus.status == "Awaiting Response":
                self.write(person.email + "<br>\n")

        return



