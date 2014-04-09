from handlers import MainHandler

class NotRegisteredHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header="Not Registered",
                            message="You are not registered.",
                            showSocial=False )

class InvalidUrlHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header="Invalid URL",
                            message="This URL is not valid.",
                            showSocial=False )

class UrlAlreadyUsedHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header="Invalid URL",
                            message="This URL has already been used.",
                            showSocial=False )
