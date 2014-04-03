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

        NewsFeedItem(
            parent=NewsFeedItem.get_default_event_parent_key(),
            description=str(urllib.unquote(self.request.get("description"))),
            highlighted=json.dumps(str(urllib.unquote(self.request.get("highlight")))),
            emergency=str(urllib.unquote(self.request.get("type")))=='emergency',
            time=int(time.time()),
            icon_url='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZWVlIj48L3JlY3Q+PHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iMzIiIHk9IjMyIiBzdHlsZT0iZmlsbDojYWFhO2ZvbnQtd2VpZ2h0OmJvbGQ7Zm9udC1zaXplOjEycHg7Zm9udC1mYW1pbHk6QXJpYWwsSGVsdmV0aWNhLHNhbnMtc2VyaWY7ZG9taW5hbnQtYmFzZWxpbmU6Y2VudHJhbCI+NjR4NjQ8L3RleHQ+PC9zdmc+'
        ).put()

        return self.redirect("/admin/mobile/newsfeed")