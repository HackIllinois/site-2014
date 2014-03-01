import MainHandler

class MGTHandler(MainHandler.Handler):
    def get(self):
        self.render("mgt.html")