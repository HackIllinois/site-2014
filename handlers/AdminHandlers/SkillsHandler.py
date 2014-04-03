import MainAdminHandler
from db.Skills import Skills
import json

class SkillsHandler(MainAdminHandler.BaseAdminTableHandler):
    def __init__(self, request, response):
        super(SkillsHandler, self).__init__(request, response)

        self.table_data = {
            'table_name': 'Mobile Skills',
            'fields': [
                {'header': 'Name', 'db_field': 'name', 'field': 'field'},
                {'header': 'Aliases', 'db_field': 'alias'},
                {'header': 'Tags', 'db_field': 'tags'}
            ],
            'content': Skills.search_database()
        }
        self.form_data = {
            'form_header': 'Add a Skill',
            'fields': [
                {'header': 'Name', 'type': 'text', 'name': 'name', 'db_field': 'name'},
                {'header': 'Aliases', 'type': 'text', 'name': 'alias', 'db_field': 'alias'},
                {'header': 'Tags', 'type': 'text', 'name': 'tags', 'db_field': 'tags'},
            ]
        }

    def get(self):
        admin_user = self.require_and_get_admin_user()

        return self.render('admin_table.html',
                           table_data=self.table_data,
                           form_data=self.form_data,
                           activePage='skills',
                           access=json.loads(admin_user.access))

    def post(self):
        self.require_and_get_admin_user()

        db_dict = self.get_db_dict()

        if 'alias' in db_dict:
            db_dict['alias'] = self.split_and_strip(db_dict['alias'])

        if 'tags' in db_dict:
            db_dict['tags'] = self.split_and_strip(db_dict['tags'])

        Skills.add_or_update(db_dict)

        return self.redirect('/admin/mobile/skills')

