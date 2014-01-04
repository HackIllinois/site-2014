import MainHandler

class ErrorHandler(MainHandler.Handler):
    """ 404 Handler """
    def get(self):
        self.redirect("/")