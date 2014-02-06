from EmailBackupHandler import EmailBackupHandler
from ErrorHandler import ErrorHandler
from IndexHandler import IndexHandler
from RegisterHandler import RegisterHandler, RegisterCompleteHandler, SchoolCheckHandler
from SignupCountHandler import SignupCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
from AdminHandler import AdminHandler
from ApproveHandler import ApproveHandler
from ProfileHandler import ProfileHandler, MyResumeHandler
# import AdminHandler
# from LoginRequiredHandler import LoginRequiredHandler


handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('/register', RegisterHandler),
    ('/register/complete', RegisterCompleteHandler),
    ('/register/schoolcheck', SchoolCheckHandler),
    ('/rules', RulesHandler),
    ('/schedule', ScheduleHandler),
    ('/signupcount', SignupCountHandler),
    ('/travel', TravelHandler),
    ('/tropo', TropoHandler),
    ('/profile', ProfileHandler.ProfileHandler),
    ('/admin', AdminHandler),
    ('/admin/approve', ApproveHandler),
    ('/profile', ProfileHandler),
    ('/profile/myresume', MyResumeHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/_ah/login_required', LoginRequiredHandler),
    ('.*', ErrorHandler)
]
