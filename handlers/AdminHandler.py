import MainHandler
import cgi, urllib, logging, re, datetime, csv
from db.Attendee import Attendee
from db.Admin import Admin
from db import constants
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import urlfetch
from collections import defaultdict
from google.appengine.api import memcache

def get_admin_user():
    user = users.get_current_user()
    if not user: return None
    admin_user = Admin.search_database({'email': user.email()}).get()
    if not admin_user: return None
    return admin_user


class AdminHandler(MainHandler.BaseAdminHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        return self.render('admin.html', data={}, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)


class AdminXkcdHandler(MainHandler.BaseAdminHandler):
    def get(self):
        xkcd_json = urlfetch.fetch('http://xkcd.com/info.0.json').content
        self.response.headers.add("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'text/json'
        return self.write(xkcd_json)


class AdminApplyCountHandler(MainHandler.BaseAdminHandler):
    def get(self):
        cached_count = memcache.get('apply_count')

        if cached_count is None:
            q = Attendee.query(Attendee.isRegistered == True)
            cached_count = q.count()
            if not memcache.add('apply_count', cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Apply Count:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.write('%d' % cached_count)


class AdminSchoolCountHandler(MainHandler.BaseAdminHandler):
    def get(self):
        cache_key = 'school_count'
        cached_count = memcache.get(cache_key)

        if cached_count is None:
            q = Attendee.query(Attendee.isRegistered == True, projection=[Attendee.school], distinct=True)
            set_of_field = set([data.school for data in q])
            cached_count = len(set_of_field)
            if not memcache.add(cache_key, cached_count, time=constants.MEMCACHE_COUNT_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('School Count:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.write('%d' % cached_count)


class AdminBasicStatsHandler(MainHandler.BaseAdminHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        data = memcache.get('basic_stats')

        if not data:
            fields = {'Schools':'school', 'Genders':'gender', 'Years':'year', 'Shirts':'shirt', 'Diets':'food', 'Projects':'projectType'}
            resume = 'Resume'

            count = 0
            collected = {}
            for f in fields:
                collected[f] = defaultdict(int)
            collected[resume] = defaultdict(int)

            hackers = Attendee.search_database({'isRegistered':True})
            for hacker in hackers:
                count += 1
                for f in fields:
                    collected[f][getattr(hacker, fields[f])] += 1

                if hacker.resume and hacker.resume.fileName:
                    collected[resume]['Has Resume'] += 1
                else:
                    collected[resume]['No Resume'] += 1

            data = {}

            data['numPeople'] = count
            if not memcache.set('apply_count', count, time=constants.MEMCACHE_COUNT_TIMEOUT):
                logging.error('Memcache set failed.')

            data['fields'] = []

            for field in sorted(collected.keys()):
                d = {}
                d['name'] = field
                d['stats'] = []
                for option in sorted(collected[field].keys()):
                    e = {}
                    e['name'] = option
                    e['num'] = collected[field][option]
                    d['stats'].append(e)
                data['fields'].append(d)

            if not memcache.add('basic_stats', data, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Basic Stats:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        return self.render('basic_stats.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)


class AdminResumeHandler(MainHandler.BaseAdminHandler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendee resumes.')

        userId = str(urllib.unquote(self.request.get('userId')))
        db_user = Attendee.search_database({'userId':userId}).get()
        if not db_user:
            return self.render( "simple_message.html",
                                header="Not Available",
                                message="User ID is not valid.",
                                showSocial=False )

        if not db_user.resume:
            return self.render( "simple_message.html",
                                header="Not Available",
                                message="User has not uploaded a resume.",
                                showSocial=False )

        # https://developers.google.com/appengine/docs/python/blobstore/#Python_Using_the_Blobstore_API_with_Google_Cloud_Storage
        resource = str(urllib.unquote(db_user.resume.gsObjectName))
        blob_key = blobstore.create_gs_key(resource)
        return self.send_blob(blob_key)


class AdminApproveHandler(MainHandler.BaseAdminHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendees.')

        data = memcache.get('hackers')
        if not data:
            hackers = Attendee.search_database({'isRegistered':True})
            data = {}
            data['hackers'] = []
            for hacker in hackers:
                data['hackers'].append({ 'nameFirst':hacker.nameFirst,
                                         'nameLast':hacker.nameLast,
                                         'email':hacker.email,
                                         'gender':hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                                         'school':hacker.school,
                                         'year':hacker.year,
                                         'linkedin':hacker.linkedin,
                                         'github':hacker.github,
                                         'shirt':hacker.shirt,
                                         'food':'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                                         'projectType':hacker.projectType,
                                         'registrationTime':hacker.registrationTime.strftime('%x %X'),
                                         'resume':hacker.resume,
                                         'isApproved':hacker.isApproved,
                                         'userId':hacker.userId})

            if not memcache.add('hackers', data, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Hackers:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.render("approve.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)

    def post(self):
        userId = str(urllib.unquote(self.request.get('userId')))
        user = Attendee.search_database({'userId':userId}).get()
        if not user:
            return self.abort(500, detail='User not in database')

        x = {}
        x['isApproved'] = str(self.request.get('isApproved')) == "True"
        success = Attendee.update_search(x, {'userId':userId})

        # Delete memcache key so /admin/approve is updated
        memcache.delete('hackers')

        return self.write(str(success))


class AdminStatsHandler(MainHandler.BaseAdminHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        schools = memcache.get('stats')

        if not schools:
            hackers = Attendee.search_database({'isRegistered':True})

            data = {}
            data['total'] = {}
            data['total']['male'] = 0
            data['total']['female'] = 0
            data['total']['other'] = 0
            data['total']['freshman'] = 0
            data['total']['sophomore'] = 0
            data['total']['junior'] = 0
            data['total']['senior'] = 0
            data['total']['grad'] = 0
            data['total']['hs'] = 0
            data['total']['xs'] = 0
            data['total']['s'] = 0
            data['total']['m'] = 0
            data['total']['l'] = 0
            data['total']['xl'] = 0
            data['total']['xxl'] = 0
            data['total']['vegetarian'] = 0
            data['total']['vegan'] = 0
            data['total']['gluten'] = 0
            data['total']['lactose'] = 0
            data['total']['otherfood'] = 0
            data['total']['software'] = 0
            data['total']['hardware'] = 0
            data['total']['unsure'] = 0

            for hacker in hackers:
                if hacker.school not in data:
                    data[hacker.school] = {}
                    data[hacker.school]['name'] = hacker.school
                    data[hacker.school]['male'] = 0
                    data[hacker.school]['female'] = 0
                    data[hacker.school]['other'] = 0
                    data[hacker.school]['freshman'] = 0
                    data[hacker.school]['sophomore'] = 0
                    data[hacker.school]['junior'] = 0
                    data[hacker.school]['senior'] = 0
                    data[hacker.school]['grad'] = 0
                    data[hacker.school]['hs'] = 0
                    data[hacker.school]['xs'] = 0
                    data[hacker.school]['s'] = 0
                    data[hacker.school]['m'] = 0
                    data[hacker.school]['l'] = 0
                    data[hacker.school]['xl'] = 0
                    data[hacker.school]['xxl'] = 0
                    data[hacker.school]['vegetarian'] = 0
                    data[hacker.school]['vegan'] = 0
                    data[hacker.school]['gluten'] = 0
                    data[hacker.school]['lactose'] = 0
                    data[hacker.school]['otherfood'] = 0
                    data[hacker.school]['software'] = 0
                    data[hacker.school]['hardware'] = 0
                    data[hacker.school]['unsure'] = 0
                if hacker.gender.lower() == 'i choose not to specify':
                    data[hacker.school]['other'] = data[hacker.school]['other'] + 1
                    data['total']['other'] = data['total']['other'] + 1
                else:
                    data[hacker.school][hacker.gender.lower()] = data[hacker.school][hacker.gender.lower()] + 1
                    data['total'][hacker.gender.lower()] = data['total'][hacker.gender.lower()] + 1
                data[hacker.school][hacker.year.lower()] = data[hacker.school][hacker.year.lower()] + 1
                data['total'][hacker.year.lower()] = data['total'][hacker.year.lower()] + 1
                data[hacker.school][hacker.shirt.lower()] = data[hacker.school][hacker.shirt.lower()] + 1
                data['total'][hacker.shirt.lower()] = data['total'][hacker.shirt.lower()] + 1
                if hacker.food:
                    for food in hacker.food.lower().split(','):
                        if food == 'other':
                            data[hacker.school]['otherfood'] = data[hacker.school]['otherfood'] + 1
                            data['total']['otherfood'] = data['total']['otherfood'] + 1
                        else:
                            data[hacker.school][food.split()[0]] = data[hacker.school][food.split()[0]] + 1
                            data['total'][food.split()[0]] = data['total'][food.split()[0]] + 1
                data[hacker.school][hacker.projectType.lower().split()[0]] = data[hacker.school][hacker.projectType.lower().split()[0]] + 1
                data['total'][hacker.projectType.lower().split()[0]] = data['total'][hacker.projectType.lower().split()[0]] + 1
            schools = {}
            schools['schools'] = []
            schools['total'] = []
            sort = []
            for x in data:
                sort.append(str(x))
            sort = sorted(sort, key=str.lower)
            for x in sort:
                if x != 'total':
                    schools['schools'].append({'name':data[x]['name'],
                                    'total':data[x]['male'] + data[x]['female'] + data[x]['other'],
                                    'male':data[x]['male'],
                                    'female':data[x]['female'],
                                    'other':data[x]['other'],
                                    'freshman':data[x]['freshman'],
                                    'sophomore':data[x]['sophomore'],
                                    'junior':data[x]['junior'],
                                    'senior':data[x]['senior'],
                                    'grad':data[x]['grad'],
                                    'hs':data[x]['hs'],
                                    'xs':data[x]['xs'],
                                    's':data[x]['s'],
                                    'm':data[x]['m'],
                                    'l':data[x]['l'],
                                    'xl':data[x]['xl'],
                                    'xxl':data[x]['xxl'],
                                    'vegetarian':data[x]['vegetarian'],
                                    'vegan':data[x]['vegan'],
                                    'gluten':data[x]['gluten'],
                                    'lactose':data[x]['lactose'],
                                    'otherfood':data[x]['otherfood'],
                                    'software':data[x]['software'],
                                    'hardware':data[x]['hardware'],
                                    'unsure':data[x]['unsure'] })
            schools['total'].append({'total':data['total']['male'] + data['total']['female'] + data['total']['other'],
                            'male':data['total']['male'],
                            'female':data['total']['female'],
                            'other':data['total']['other'],
                            'freshman':data['total']['freshman'],
                            'sophomore':data['total']['sophomore'],
                            'junior':data['total']['junior'],
                            'senior':data['total']['senior'],
                            'grad':data['total']['grad'],
                            'hs':data['total']['hs'],
                            'xs':data['total']['xs'],
                            's':data['total']['s'],
                            'm':data['total']['m'],
                            'l':data['total']['l'],
                            'xl':data['total']['xl'],
                            'xxl':data['total']['xxl'],
                            'vegetarian':data['total']['vegetarian'],
                            'vegan':data['total']['vegan'],
                            'gluten':data['total']['gluten'],
                            'lactose':data['total']['lactose'],
                            'otherfood':data['total']['otherfood'],
                            'software':data['total']['software'],
                            'hardware':data['total']['hardware'],
                            'unsure':data['total']['unsure'] })

            if not memcache.add('stats', schools, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Advanced Stats:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.render("stats.html", schools=schools, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)


class AdminProfileHandler(MainHandler.BaseAdminHandler):
    def get(self, userId):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to view attendee profiles.')

        userId = str(urllib.unquote(userId))
        db_user = Attendee.search_database({'userId':userId}).get()
        # TODO: add sanity check for user exists

        data = {}
        text_fields = [
            'nameFirst', 'nameLast', 'email', 'school',
            'experience', 'linkedin', 'github', 'year',
            'gender', 'projectType', 'shirt', 'food',
            'foodInfo', 'teamMembers', 'registrationTime',
            'userNickname', 'userEmail', 'userId', 'isApproved', 'resume'
        ]

        for field in text_fields:
            value = getattr(db_user, field) # Gets db_user.field using a string
            if value is not None: data[field] = value

        return self.render("admin_profile.html", data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)

class AdminEditProfileHandler(MainHandler.BaseAdminHandler):
    def get(self, userId):
        userId = str(urllib.unquote(userId))
        db_user = Attendee.search_database({'userId':userId}).get()
        return self.write(db_user.email)

    def post(self, userId):
        userId = str(urllib.unquote(userId))
        db_user = Attendee.search_database({'userId':userId}).get()
        return self.write(db_user.email)


class AdminManagerHandler(MainHandler.BaseAdminHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')

        db_admins = Admin.search_database({})
        admins = [ {'email':admin.email, 'approveAccess':admin.approveAccess, 'fullAccess':admin.fullAccess} for admin in db_admins ]
        data = {'admins':admins}
        return self.render('admin_manager.html', data=data, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)


class AdminAccessControlHandler(MainHandler.BaseAdminHandler):
    def post(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.fullAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        email = str(urllib.unquote(self.request.get('email')))
        accessControl = self.request.get('accessControl')
        approveAccess = accessControl == 'approve'
        fullAccess = accessControl == 'full'

        db_user = Admin.search_database({'email': email}).get()
        if not db_user:
            Admin.add({'approveAccess':(approveAccess or fullAccess),
                       'fullAccess':fullAccess,
                       'email': email})
        else:
            Admin.update_search({'approveAccess':(approveAccess or fullAccess),
                                 'fullAccess':fullAccess},
                                {'email': email})

        return self.redirect('/admin/manager')


class AdminExportHandler(MainHandler.BaseAdminHandler):
    def get(self):
        admin_user = get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to download attendees csv.')


        data = memcache.get('hackers')
        if not data:
            hackers = Attendee.search_database({'isRegistered':True})
            data = {}
            data['hackers'] = []
            for hacker in hackers:
                data['hackers'].append({ 'nameFirst':hacker.nameFirst,
                                         'nameLast':hacker.nameLast,
                                         'email':hacker.email,
                                         'gender':hacker.gender if hacker.gender == 'Male' or hacker.gender == 'Female' else 'Other',
                                         'school':hacker.school,
                                         'year':hacker.year,
                                         'linkedin':hacker.linkedin,
                                         'github':hacker.github,
                                         'shirt':hacker.shirt,
                                         'food':'None' if not hacker.food else ', '.join(hacker.food.split(',')),
                                         'projectType':hacker.projectType,
                                         'registrationTime':hacker.registrationTime.strftime('%x %X'),
                                         'resume':hacker.resume,
                                         'isApproved':hacker.isApproved,
                                         'userId':hacker.userId})

            if not memcache.add('hackers', data, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Hackers:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))


        dt = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment;filename=' + dt + '-attendees.csv'

        hackers = data['hackers']

        writer = csv.writer(self.response.out)
        writer.writerow(constants.CSV_HEADINGS)
        for h in hackers:
            writer.writerow([ h['nameFirst'],
                              h['nameLast'],
                              h['email'],
                              h['gender'],
                              h['school'],
                              h['year'],
                              h['linkedin'],
                              h['github'],
                              h['shirt'],
                              h['food'],
                              h['projectType'],
                              h['registrationTime'],
                              h['resume'],
                              h['isApproved'],
                              h['userId'] ])
        return
