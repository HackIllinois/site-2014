import MainAdminHandler
from db.Skills import Skills

class AddingSkillsHandler(MainAdminHandler.BaseAdminHandler):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        
        return self.render('skills.html', data={}, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)
    
    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user: return self.abort(500, detail='User not in database')
        
        name = self.request.get('name')
        alias = self.request.get('alias')
        tags = self.request.get('tags')
        
        aliasList = alias.split(',')
        tagsList = tags.split(',')
        
        skillsDict = {'name':name, 'alias':aliasList, 'tags':tagsList}

        print 'skills dict %s' % skillsDict

        Skills.add(skillsDict)
        return self.render('skills.html', data={}, approveAccess=admin_user.approveAccess, fullAccess=admin_user.fullAccess)