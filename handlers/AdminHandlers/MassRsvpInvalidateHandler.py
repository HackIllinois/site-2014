import MainAdminHandler
from db import constants
from db.Attendee import Attendee
import re
import urllib
from datetime import datetime
import json

class MassRsvpInvalidateHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAdminAccess:
            return self.abort(401, detail='User does not have permission to mass invalidate rsvps.')

        data = {}
        return self.render('admin_mass_invalidate_rsvp.html', data=data, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAdminAccess:
            return self.abort(401, detail='User does not have permission to rsvp invalidate.')

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

        successful_emails = []
        not_found_emails = []
        not_yet_emailed_emails = []
        already_rsvpd_emails = []
        already_invalid_emails = []
        error_emails = []
        for email in valid_emails:
            person = Attendee.search_database({'email': email}).get()
            if not person:
                person = Attendee.search_database({'userEmail': email}).get()
                if not person:
                    not_found_emails.append(email)
                    continue

            if person.approvalStatus.status == "Awaiting Response":
                successful_emails.append(email)
                person.approvalStatus.status = "No Rsvp"
                person.approvalStatus.rsvpInvalidTime = datetime.now()
                person.put()
            elif person.approvalStatus.status in ["Rsvp Coming","Rsvp Not Coming"]:
                already_rsvpd_emails.append(email)
            elif person.approvalStatus.status == "No Rsvp":
                already_invalid_emails.append(email)
            else:
                error_emails.append(email)

        self.write("Successful Emails: %s<br>" % str(successful_emails))
        self.write("Not Found Emails: %s<br>" % str(not_found_emails))
        self.write("Not Yet Emailed Emails: %s<br>" % str(not_yet_emailed_emails))
        self.write("Already RSVP'd Emails: %s<br>" % str(already_rsvpd_emails))
        self.write("Already Invalid Emails: %s<br>" % str(already_invalid_emails))
        self.write("Error Emails: %s<br>" % str(error_emails))
        return
