import MainHandler
import cgi
import db.models as models
import logging
from google.appengine.api import users

class RegisterHandler(MainHandler.Handler):
    """ Handler for registration page.
    This does not include the email registration we have up now."""
    def get(self):
        # TODO: Check if user is already registered and redirect to /profile

        user = users.get_current_user()
        if user:
            db_user = models.search_database(models.Attendee, {'userId':user.user_id()}).get()
            if db_user is not None:
                return self.redirect('/profile')
            else:
                data = {}
                data['username'] = user.nickname()
                data['logoutUrl'] = users.create_logout_url('/register')
                data['email'] = user.email()
                self.render("register.html", data=data)
        else:
            # This should never happen
            self.render("register.html", data={'email':None})

    def post(self):
        user = users.get_current_user()
        if user:
            x = {}

            # https://developers.google.com/appengine/docs/python/users/userclass
            x['userNickname'] = user.nickname()
            x['userEmail'] = user.email()
            x['userId'] = user.user_id()
            x['userFederatedIdentity'] = user.federated_identity()
            x['userFederatedProvider'] = user.federated_provider()

            x['nameFirst'] = self.request.get('nameFirst')
            x['nameLast'] = self.request.get('nameLast')
            x['email'] = self.request.get('email')
            x['gender'] = self.request.get('gender')
            x['school'] = self.request.get('school')
            if x['school'] == 'Other':
                x['school'] = self.request.get('schoolOther')
            x['standing'] = self.request.get('year')

            x['experience'] = self.request.get('experience')
            x['resume'] = str(self.request.get('resume'))
            x['linkedin'] = self.request.get('linkedin')
            x['github'] = self.request.get('github')

            x['shirt'] = self.request.get('shirt')
            x['food'] = self.request.get('food')

            x['teamMembers'] = self.request.get('team')

            x['recruiters'] = (self.request.get('recruiters') == 'True')
            x['picture'] = (self.request.get('picture') == 'True')
            x['termsOfService'] = (self.request.get('termsOfService') == 'True')

            models.add(models.Attendee, x)
            logging.info('Signup with email %s', x['email'])

            self.render("registration_complete.html")
        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR')