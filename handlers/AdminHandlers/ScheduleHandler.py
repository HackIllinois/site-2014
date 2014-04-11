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


        feed = Schedule.query(ancestor=Schedule.get_default_event_parent_key()).order(-Schedule.time)

        #print feed
        return self.render("admin_mobile_schedule.html", feed=feed, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')



        #check all fields valid

        Schedule(
            event_name=self.request.get('event_name'),
            description=self.request.get('description'),
            location=self.request.get("location"),
            time=int(time.time()),
            icon_url= self.request.get('img_src'),
            day = str(urllib.unquote(self.request.get('day')))
        ).put()

        return self.write(json.dumps({'message':'success'}))