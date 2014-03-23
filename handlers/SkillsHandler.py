import MainHandler

class RenderHandler(MainHandler.Handler):
    """ Handler for the mentor skills page """

    def get(self):
        SkillsData = {} #adding dummy data for now, please change this
        SkillsData['errors'] = ""

        
        SkillsData['skillsList'] = ""
        SkillsData['skillsTags1'] = ""
        SkillsData['skillsTags2'] = ""
        SkillsData['skillsTags3'] = ""
        self.render("skills.html", data=SkillsData)

    def post(self):
    	print('post')

