import MainAdminHandler
import json
import urllib
import time
import datetime

from db.Schedule import Schedule
from db.Room import Room
from db.MobileConstants import MAP

class ScheduleHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')

        q = Schedule.query(ancestor=Schedule.get_default_event_parent_key()).order(-Schedule.time)

        feed = []
        for i in q:
            feed.append({
                "img":{"alt":"", "src":i.icon_url },
                "event_name":i.event_name,
                "description":i.description,
                "location":i.room_obj["room_number"],
                "time":i.day
            })

        print feed

        return self.render("admin_mobile_schedule.html", feed=feed, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')


        #create room from request
        roomnumber = self.request.get('location')
        rooms = filter(lambda x: x['room_number'] == roomnumber, MAP)

        #check all fields valid
        schedule_item = Schedule(
            parent=Schedule.get_default_event_parent_key(),
            event_name=self.request.get('event_name'),
            description=self.request.get('description'),
            room_obj=rooms[0],
            icon_url='http://www.hackillinois.org/'+self.request.get('img_src'),
            day=str(urllib.unquote(self.request.get('day')))
        )

        if schedule_item.day == 'Friday':
            s = "11/04/2014" + " " + self.request.get('time')
            schedule_item['time'] = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y %H:%M").timetuple())
        elif schedule_item.day == 'Saturday':
            s = "12/04/2014" + " " + self.request.get('time')
            schedule_item['time'] = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y %H:%M").timetuple())
        elif schedule_item.day == 'Sunday':
            s = "13/04/2014" + " " + self.request.get('time')
            schedule_item['time'] = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y %H:%M").timetuple())

        self.response.headers['Content-Type'] = 'application/json'
        return self.response.write(json.dumps({'message':'success'}))
