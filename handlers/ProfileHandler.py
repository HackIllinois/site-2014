import MainHandler
import db.models as models
from google.appengine.api import users

class ProfileHandler(MainHandler.Handler):

    def get(self):
        user = users.get_current_user()
        if user:
            db_user = models.search_database(models.Attendee, {'userId':user.user_id()}).get()
            if db_user is None:
                return self.redirect('/register')
            # TODO: if user not in system, redirect to /register

            data = {}
            data['username'] = user.nickname()
            data['logoutUrl'] = users.create_logout_url('/')
            data['nameFirst'] = db_user.nameFirst
            data['nameLast'] = db_user.nameLast
            data['email'] = db_user.email
            data['genders'] = [ {'name':'Male', 'checked':False},
                                {'name':'Female', 'checked':False},
                                {'name':'N/A', 'checked':False} ]
            for i in data['genders']:
                if i['name'] == db_user.gender:
                    i['checked'] = True
                    break
            data['schools'] = [ {'name':'University of Illinois at Urbana-Champaign', 'selected':False},
                                {'name':'Massachusetts Institute of Technology', 'selected':False},
                                {'name':'Stanford University', 'selected':False},
                                {'name':'University of California, Berkeley', 'selected':False},
                                {'name':'California Institute of Technology', 'selected':False},
                                {'name':'Georgia Institute of Technology', 'selected':False},
                                {'name':'Carnegie Mellon University', 'selected':False},
                                {'name':'Cornell University', 'selected':False},
                                {'name':'University of Michigan, Ann Arbor', 'selected':False},
                                {'name':'Purdue University, West Lafayette', 'selected':False},
                                {'name':'University of Texas at Austin', 'selected':False},
                                {'name':'University of Wisconsin, Madison', 'selected':False},
                                {'name':'Princeton University', 'selected':False},
                                {'name':'University of Washington', 'selected':False},
                                {'name':'Other', 'selected':False} ]
            for i in data['schools']:
                if i['name'] == db_user.school:
                    i['selected'] = True
                    break
            data['years'] = [ {'name':'Freshman', 'checked':False},
                              {'name':'Sophomore', 'checked':False},
                              {'name':'Junior', 'checked':False},
                              {'name':'Senior', 'checked':False} ]
            for i in data['years']:
                if i['name'] == db_user.standing:
                    i['checked'] = True
                    break
            data['experience'] = db_user.experience
            data['linkedin'] = db_user.linkedin
            data['github'] = db_user.github
            data['shirts'] = [ {'name':'XS', 'checked':False},
                               {'name':'S', 'checked':False},
                               {'name':'M', 'checked':False},
                               {'name':'L', 'checked':False},
                               {'name':'XL', 'checked':False},
                               {'name':'XXL', 'checked':False} ]
            for i in data['shirts']:
                if i['name'] == db_user.shirt:
                    i['checked'] = True
                    break
            data['foods'] = [ {'name':'None', 'checked':False},
                              {'name':'Vegetarian', 'checked':False},
                              {'name':'Vegan', 'checked':False},
                              {'name':'Gluten Free', 'checked':False} ]
            for i in data['foods']:
                if i['name'] == db_user.food:
                    i['checked'] = True
                    break
            data['team'] = db_user.teamMembers
            data['recruiters'] = db_user.recruiters
            data['picture'] = db_user.picture
            data['termsOfService'] = db_user.termsOfService

            self.render('profile.html', data=data)

        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR')

    def post(self):
        user = users.get_current_user()
        if user:
            x = {}

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

            models.update_search(models.Attendee, x, {'userId':user.user_id()})

            self.render("update_successful.html")
        else:
            # User not logged in (shouldn't happen)
            # TODO: redirect to error handler
            self.write('ERROR')
