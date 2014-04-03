import MainAdminHandler
from db.Admin import Admin
from db.Whitelist import Whitelist

import urllib

class ManagerHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.fullAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        data = {}

        db_admins = Admin.search_database({})
        data['admins'] = [ {'email':admin.email, 'approveAccess':admin.approveAccess, 'fullAccess':admin.fullAccess, 'mobileAccess':admin.mobileAccess} for admin in db_admins ]

        db_whtlsts = Whitelist.search_database({})
        whitelists = [ {'enabled': w.enabled,
                        'url': self.request.host_url+'/apply/whitelist/'+w.uniqueString,
                        'intendedRecipientEmail': w.intendedRecipientEmail,
                        'creationTime': w.creationTime.strftime('%x %X'),
                        'userEmail': w.userEmail,
                        'registerTime': w.registerTime.strftime('%x %X') if w.registerTime else None
                        } for w in db_whtlsts ]
        data['whitelists'] = whitelists

        return self.render('admin_manager.html', data=data, approveAccess=admin_user.approveAccess, mobileAccess=admin_user.mobileAccess, fullAccess=admin_user.fullAccess)

class WhitelistControlHandler(MainAdminHandler.BaseAdminHandler):
    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        if not admin_user.fullAccess:
            return self.abort(401, detail='User does not have permission to edit admin permissions.')

        intendedRecipientEmail = str(urllib.unquote(self.request.get('email')))
        enabled = self.request.get('whitelistControl') == 'True'

        db_whtlst = Whitelist.search_database({'intendedRecipientEmail': intendedRecipientEmail}).get()
        if not db_whtlst:
            Whitelist.add({'intendedRecipientEmail': intendedRecipientEmail, 'enabled': enabled})
        else:
            Whitelist.update_search({'enabled': enabled}, {'intendedRecipientEmail': intendedRecipientEmail})

        return self.redirect('/admin/manager')
