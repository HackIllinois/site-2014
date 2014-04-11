import MainAdminHandler
import json
import urllib
import time
from db.Schedule import Schedule

class ScheduleHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')

        feed = []

        for num in range(10):
          feed.append(
          {
          "event_name" : "A fine Event {}".format(num) ,
          "description" : "kajsdnfkansdfjkansdjkfnaskjdfnasjkdfnjasdnf",
          "location" : "1404 SC",
          "time" : time.time(),
          "icon_url" : "http://www.hackillinois.org/img/icons-iOS/emergency.png",
          "day" : "Friday"
          }
          )

        #items = Schedule.query(ancestor=Schedule.get_default_event_parent_key()).order(-Schedule.time)


        #print feed
        return self.render("admin_mobile_schedule.html", feed=feed, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')


        icon = {
            'emergency':'http://www.hackillinois.org/img/icons-iOS/emergency.png',
            'announcement':'http://www.hackillinois.org/img/icons-iOS/announce.png',
            'hackillinois':'http://www.hackillinois.org/img/icons-iOS/hackillinois.png',
        }

        colors = {
            'emergency':{'r':167, 'g':65, 'b':46},
            'announcement':{'r':165, 'g':165, 'b':165},
            'hackillinois':{'r':27, 'g':77, 'b':104},
        }

        #check all fields valid
        event_name = self.request.get('event_name')
        if not event_name or event_name == "":
          return self.write(json.dumps({'message':'You Must Supply an Event Name'}))

        description = self.request.get("description")


        Schedule(
            event_name=NewsFeedItem.get_default_event_parent_key(),
            description=description,
            location=self.request.get("location"),
            time=int(time.time()),
            icon_url=icon[str(urllib.unquote(self.request.get("type")))],
            day = str(urllib.unquote(self.request.get('day')))
        ).put()

        return self.write(json.dumps({'message':'success'}))