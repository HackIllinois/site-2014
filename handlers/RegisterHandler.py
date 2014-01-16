import MainHandler
import cgi
import db.models as models
import logging

class RegisterHandler(MainHandler.Handler):
    """ Handler for registration page.
    This does not include the email registration we have up now."""
    def get(self):
        self.render("register.html")

    def post(self):
        x = {}

        x['nameFirst'] = cgi.escape(self.request.get('nameFirst'))
        x['nameLast'] = cgi.escape(self.request.get('nameLast'))
        x['email'] = cgi.escape(self.request.get('email'))
        x['gender'] = cgi.escape(self.request.get('gender'))
        x['school'] = cgi.escape(self.request.get('school'))
        if x['school'] == 'Other':
            x['school'] = cgi.escape(self.request.get('schoolOther'))
        x['standing'] = cgi.escape(self.request.get('year'))

        x['experience'] = cgi.escape(self.request.get('experience'))
        # x['resume'] = self.request.get('resume')
        x['linkedin'] = cgi.escape(self.request.get('linkedin'))
        x['github'] = cgi.escape(self.request.get('github'))

        x['shirt'] = cgi.escape(self.request.get('shirt'))
        x['food'] = cgi.escape(self.request.get('food'))

        x['teamMembers'] = cgi.escape(self.request.get('team'))

        r = cgi.escape(self.request.get('recruiters'))
        if r == 'True':
            x['recruiters'] = True
        p = cgi.escape(self.request.get('picture'))
        if p == 'True':
            x['picture'] = True
        t = cgi.escape(self.request.get('termsOfService'))
        if t == 'True':
            x['termsOfService'] = True

        models.add(models.Attendee, x)
        logging.info('Signup with email %s', x['email'])

        self.render("registration_complete.html")