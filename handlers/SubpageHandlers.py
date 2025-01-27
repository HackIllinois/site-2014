import MainHandler

""" This puts all the very simple subpage handlers in one place. If these start getting logic, move them into their own files. :D """

class RulesHandler(MainHandler.Handler):
    """ Handler for the rules subpage """
    def get(self):
        self.render("rules.html")

class ScheduleHandler(MainHandler.Handler):
    """ Handler for the schedule subpage """
    def get(self):
        self.render("schedule.html")

class TravelHandler(MainHandler.Handler):
    """ Handler for the travel subpage """
    def get(self):
        self.render("travel.html")

class CoCHandler(MainHandler.Handler):
    """ Handler for the code of conduct subpage """
    def get(self):
        self.render("code-of-conduct.html")

class StaffHandler(MainHandler.Handler):
    """ Handler for the staff subpage """
    def get(self):
        self.render("staff.html")

class SponsorFAQHandler(MainHandler.Handler):
    """ Handler for the sponsor FAQ subpage """
    def get(self):
        self.render("sponsor_faq.html")

class AppsPageHandler(MainHandler.Handler):
    """ Handler for the apps FAQ subpage """
    def get(self):
        self.render("apps.html")