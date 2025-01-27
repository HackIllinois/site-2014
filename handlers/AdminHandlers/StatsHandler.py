import MainAdminHandler
import logging
from db.Attendee import Attendee
from db import constants
from google.appengine.api import memcache
import json


class StatsHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
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

            if not memcache.set('stats', schools, time=constants.MEMCACHE_TIMEOUT):
                logging.error('Memcache set failed.')

        stats = memcache.get_stats()
        logging.info('Advanced Stats:: Cache Hits:%s  Cache Misses:%s' % (stats['hits'], stats['misses']))

        self.render("stats.html", schools=schools, access=json.loads(admin_user.access))
