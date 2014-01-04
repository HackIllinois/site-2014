import MainHandler

class RegisterHandler(MainHandler.Handler):
    """ Handler for registration page.
    This does not include the email registration we have up now."""
    def get(self):
        self.render("register.html")

    def post(self):
        name = self.request.get('name')
        if not name:
            self.write("No registration name.")
            return

        self.write("Thanks for registering, " + name + "!")
        return