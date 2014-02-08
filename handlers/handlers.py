from EmailBackupHandler import EmailBackupHandler
from ErrorHandler import ErrorHandler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, ApplyCountHandler, SchoolCheckHandler, SchoolListHandler, MyResumeHandler, UpdateCompleteHandler
from SignupCountHandler import SignupCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
# import AdminHandler
# from LoginRequiredHandler import LoginRequiredHandler


handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('/apply/?', ApplyHandler),
    ('/apply/complete', ApplyCompleteHandler),
    ('/apply/updated', UpdateCompleteHandler),
    ('/apply/schoolcheck', SchoolCheckHandler),
    ('/apply/schoollist', SchoolListHandler),
    ('/apply/myresume', MyResumeHandler),
    ('/applycount', ApplyCountHandler),
    ('/rules', RulesHandler),
    ('/schedule', ScheduleHandler),
    ('/signupcount', SignupCountHandler),
    ('/travel', TravelHandler),
    ('/tropo', TropoHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/admin', AdminHandler.AdminHandler),
    ('.*', ErrorHandler)
]
