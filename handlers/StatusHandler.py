import MainHandler
import json
import urllib
import time
import re
from db.NewsFeedItem import NewsFeedItem

class StatusHandler(MainHandler.Handler):
    def highlight_description(self, description, highlight):
        return description

    def get(self):
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
                'time':time.strftime("%I:%M %p, %A",time.localtime(item.time-5*60*60)),
                'heading':'Emergency' if item.emergency else 'Update' if item.hackillinois else 'Announcement' if item.announcement else 'Info'
            })
        # Don't do this. It floods the logs. --Matthew
        # print feed
        return self.render("status.html", feed=feed)