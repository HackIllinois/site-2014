from EmailBackupHandler import EmailBackupHandler
from ErrorHandler import ErrorHandler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, SchoolCheckHandler, SchoolListHandler
from SignupCountHandler import SignupCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
from ProfileHandler import ProfileHandler, MyResumeHandler, UpdateCompleteHandler
# import AdminHandler
# from LoginRequiredHandler import LoginRequiredHandler


handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('/apply/?', ApplyHandler),
    ('/apply/complete', ApplyCompleteHandler),
    ('/apply/schoolcheck', SchoolCheckHandler),
    ('/apply/schoollist', SchoolListHandler),
    ('/rules', RulesHandler),
    ('/schedule', ScheduleHandler),
    ('/signupcount', SignupCountHandler),
    ('/travel', TravelHandler),
    ('/tropo', TropoHandler),
    ('/profile/?', ProfileHandler),
    ('/profile/updated', UpdateCompleteHandler),
    ('/profile/myresume', MyResumeHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/admin', AdminHandler.AdminHandler),
    # ('/_ah/login_required', LoginRequiredHandler),
    ('.*', ErrorHandler)
]
