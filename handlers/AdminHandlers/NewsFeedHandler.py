import MainAdminHandler
import json
import urllib
import time
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

        NewsFeedItem(
            parent=NewsFeedItem.get_default_event_parent_key(),
            description=str(urllib.unquote(self.request.get("description"))),
            highlighted=json.dumps(str(urllib.unquote(self.request.get("highlight")))),
            emergency=str(urllib.unquote(self.request.get("type")))=='emergency',
            time=int(time.time()),
            icon_url=icon[str(urllib.unquote(self.request.get("type")))]
        ).put()

        return self.redirect("/admin/mobile/newsfeed")