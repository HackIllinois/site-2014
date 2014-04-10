import MainAdminHandler
import json
import urllib
import time
import re
from db.NewsFeedItem import NewsFeedItem

class NewsFeedHandler(MainAdminHandler.BaseAdminHandler):
    def highlight_description(self, description, highlight):
        return description

    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')

        feed = []
        items = NewsFeedItem.query(ancestor=NewsFeedItem.get_default_event_parent_key()).order(-NewsFeedItem.time)
        for item in items:
            description = self.highlight_description(item.description, item.highlighted)
            feed.append({
                'description':description,
                'img':{
                    'alt':'Emergency' if item.emergency else 'HackIllinois',
                    'src':item.icon_url,
                },
            })
        print feed
        return self.render("admin_mobile_news_feed.html", feed=feed, access=json.loads(admin_user.access))

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

        description = str(urllib.unquote(self.request.get("description")))

        hl = str(urllib.unquote(self.request.get("highlight")))
        hl = hl.strip()
        if not hl:
            hl = None
        else:
            hl = re.sub(r'[\(\)\[\]]', '', hl)
            hl = re.split(r'[,; ]', hl)
            hl = [i.strip() for i in hl]
            hl = filter(None, hl)
            try:
                hl = map(int, hl)
            except:
                return self.write(json.dumps({'message':'Error: highlights must be integer values'}))

            strictly_increasing = all(x<y for x, y in zip(hl, hl[1:]))
            if not strictly_increasing:
                return self.write(json.dumps({'message':'Error: highlights overlap'}))

            if (len(hl) % 2) != 0:
                return self.write(json.dumps({'message':'Error: highlights are not paired'}))

            if hl[0] < 0:
                return self.write(json.dumps({'message':'Error: highlight goes beyond length of description'}))

            if hl[-1] > (len(description)-1):
                return self.write(json.dumps({'message':'Error: highlight goes beyond length of description'}))

        # [ [ [start,end],[r,g,b] ], [ [start,end],[r,g,b] ] ]


        NewsFeedItem(
            parent=NewsFeedItem.get_default_event_parent_key(),
            description=description,
            highlighted=hl,
            emergency=str(urllib.unquote(self.request.get("type")))=='emergency',
            time=int(time.time()),
            icon_url=icon[str(urllib.unquote(self.request.get("type")))]
        ).put()

        return self.write(json.dumps({'message':'success'}))