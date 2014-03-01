import MainHandler

class MGTHandler(MainHandler.Handler):
    def get(self):
        self.render("mgt.html")

class ParticlesHandler(MainHandler.Handler):
    def get(self):
        self.render("particles.html")