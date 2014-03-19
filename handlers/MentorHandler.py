import MainHandler

class RenderHandler(MainHandler.Handler):

    def get(self):
        MentorData = {} #adding dummy data for now, please change this
        MentorData['errors'] = {} # Needed for template to render


        MentorData['nameFirst'] = "First Name"
        MentorData['nameLast'] = "Last Name"
        MentorData['company'] = "Mentor Company"
        MentorData['email'] = "Mentor email"
        MentorData['jobTitle'] = "Mentor Job Title"
        MentorData['skills'] = "No Skills at all. JK."

        self.render("mentor.html", data=MentorData)

