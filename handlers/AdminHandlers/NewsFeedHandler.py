import MainAdminHandler
import json

class NewsFeedHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            return self.abort(500, detail='User not in database')
        if not admin_user.mobileAccess:
            return self.abort(401, detail='User does not have permission to update the mobile newsfeed.')

        data = {}
        return self.render("admin_mobile_news_feed.html", data=data, access=json.loads(admin_user.access))

    def post(self):
        
        # description
        # time
        # icon_url
        # highlighted
        # emergency

        pass