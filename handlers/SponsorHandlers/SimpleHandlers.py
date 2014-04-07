from handlers import MainHandler

class NotRegisteredHandler(MainHandler.Handler):
    def get(self):
        return self.render( "simple_message.html",
                            header="Not Registered",
                            message="You are not registered.",
                            showSocial=False )
