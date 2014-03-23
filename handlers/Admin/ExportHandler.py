import MainAdminHandler

import datetime

class ExportHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.approveAccess:
            return self.abort(401, detail='User does not have permission to download attendees csv.')

        dt = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment;filename=' + dt + '-attendees.csv'

        return self.write(self.get_hackers_csv_memcache(self.request.application_url))