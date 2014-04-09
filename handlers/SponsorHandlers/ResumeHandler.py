import MainSponsorHandler

class ResumeHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        return self.write("Resume")
