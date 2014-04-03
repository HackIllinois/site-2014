import MainAdminHandler
from db import constants
from db.Attendee import Attendee
import re
import urllib
from datetime import datetime
# import requests
import json

class MassApprovalHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAdminAccess:
            return self.abort(401, detail='User does not have permission to mass approve.')

        data = {}
        return self.render('admin_mass_approval.html', data=data, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAdminAccess:
            return self.abort(401, detail='User does not have permission to email attendees.')

        action = str(urllib.unquote(self.request.get('action')))

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
        already_approved_emails = []
        already_emailed_emails = []
        error_emails = []

        found_emails = {}
        for email in valid_emails:
            found_emails[email] = True

        hackers = Attendee.query(Attendee.email.IN(valid_emails))

        for person in hackers:
            del found_emails[person.email]
            if person.approvalStatus.status in ["Not Approved", "Waitlisted"]:
                successful_emails.append(email)
                if action == "approve":
                    person.approvalStatus.status = "Approved"
                    person.approvalStatus.approvedTime = datetime.now()
                    person.put()
                elif action == "waitlist":
                    person.approvalStatus.status = "Waitlisted"
                    person.approvalStatus.waitlistedTime = datetime.now()
                    person.put()
                else:
                    return self.write("Error: Invalid action.")
            elif person.approvalStatus.status == "Approved":
                already_approved_emails.append(email)
            elif person.approvalStatus.status in constants.RSVP_STATUSES:
                already_emailed_emails.append(email)
            else:
                error_emails.append(email)

        for email in found_emails:
            not_found_emails.append(email)

        self.write("Successful Emails: %s<br>" % str(successful_emails))
        self.write("Not Found Emails: %s<br>" % str(not_found_emails))
        self.write("Already Approved Emails: %s<br>" % str(already_approved_emails))
        self.write("Already Emailed Emails: %s<br>" % str(already_emailed_emails))
        self.write("Error Emails: %s<br>" % str(error_emails))

        # Integrate with the SendGrid API to actually send the emails!
        # self.write("Email Status: %s<br>" % self.send_acceptance_email(successful_emails))

        return
