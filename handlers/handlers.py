from EmailBackupHandler import EmailBackupHandler
from ErrorHandler import ErrorHandler
from IndexHandler import IndexHandler
from RegisterHandler import RegisterHandler, RegisterCompleteHandler
from SignupCountHandler import SignupCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
import ProfileHandler
# import AdminHandler
# from LoginRequiredHandler import LoginRequiredHandler


handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('/register', RegisterHandler),
    ('/register/complete', RegisterCompleteHandler),
    ('/rules', RulesHandler),
    ('/schedule', ScheduleHandler),
    ('/signupcount', SignupCountHandler),
    ('/travel', TravelHandler),
    ('/tropo', TropoHandler),
    ('/profile', ProfileHandler.ProfileHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/admin', AdminHandler.AdminHandler),
    # ('/_ah/login_required', LoginRequiredHandler),
    ('.*', ErrorHandler)
]
