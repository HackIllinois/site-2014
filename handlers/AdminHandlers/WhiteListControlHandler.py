import MainAdminHandler
from db.Admin import Admin
from db.Whitelist import Whitelist

import urllib
import json

class WhitelistControlHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        data = {}

        db_whtlsts = Whitelist.search_database({})
        whitelists = [ {'enabled': w.enabled,
                        'url': self.request.host_url+'/apply/whitelist/'+w.uniqueString,
                        'intendedRecipientEmail': w.intendedRecipientEmail,
                        'creationTime': w.creationTime.strftime('%x %X'),
                        'userEmail': w.userEmail,
                        'registerTime': w.registerTime.strftime('%x %X') if w.registerTime else None
                        } for w in db_whtlsts ]
        data['whitelists'] = whitelists

        return self.render('admin_whitelist.html', data=data, access=json.loads(admin_user.access))

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.managerAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        intendedRecipientEmail = str(urllib.unquote(self.request.get('email')))
        enabled = self.request.get('whitelistControl') == 'True'

        db_whtlst = Whitelist.search_database({'intendedRecipientEmail': intendedRecipientEmail}).get()
        if not db_whtlst:
            Whitelist.add({'intendedRecipientEmail': intendedRecipientEmail, 'enabled': enabled})
        else:
            Whitelist.update_search({'enabled': enabled}, {'intendedRecipientEmail': intendedRecipientEmail})

        return self.redirect('/admin/whitelist')
