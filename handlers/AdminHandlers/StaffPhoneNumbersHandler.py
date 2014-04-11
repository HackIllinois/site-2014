import MainAdminHandler
from db import constants
from db.PhoneNumber import PhoneNumber
import re
import urllib
from datetime import datetime
# import requests
import json

class StaffPhoneNumbersHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to edit stapff phone number list.')

        q = PhoneNumber.query(
            PhoneNumber.groups == "Staff",
            ancestor=PhoneNumber.get_default_event_parent_key()
        )
        numbers = [ {"number": i.number, "groups": i.groups} for i in q ]
        numbers = sorted(numbers, key=lambda n: len(n["groups"]), reverse=True)

        return self.render('admin_staff_phone_numbers.html', numbers=numbers, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to edit stapff phone number list.')

        numbers = str(urllib.unquote(self.request.get('numbers')))
        sendAccess = self.request.get('sendAccess') == 'True'

        numbers = numbers.strip()
        if not numbers:
            return self.write("Error: No numbers entered.")

        # Split emails by comma, semicolon, space, or newline (or some combination of all of those)
        numbers = re.split(r'[,; \n]', numbers)

        numbers = [ numbers[i].strip() for i in xrange(len(numbers)) ]

        valid_numbers = []
        invalid_numbers = []
        for number in numbers:
            if re.match(constants.PHONE_MATCH, number):
                valid_numbers.append(number)
            else:
                invalid_numbers.append(number)

        successful_numbers = []
        already_exists_numbers = []

        for number in valid_numbers:
            q = PhoneNumber.query(
                PhoneNumber.number == number,
                ancestor=PhoneNumber.get_default_event_parent_key()
            )
            if q.count() > 0:
                already_exists_numbers.append(number)
            else:
                successful_numbers.append(number)
                PhoneNumber(
                    parent=PhoneNumber.get_default_event_parent_key(),
                    number=number,
                    groups=["Staff"] if not sendAccess else ["Staff", "SendStaff"]
                ).put()


        self.write("Successful Numbers: %s<br>" % str(successful_numbers))
        self.write("Already Exists Numbers: %s<br>" % str(already_exists_numbers))
        self.write("Invalid Numbers: %s<br>" % str(invalid_numbers))

        return
