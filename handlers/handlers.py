from EmailBackupHandler import EmailBackupHandler
from ErrorHandler import ErrorHandler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, SchoolCheckHandler, SchoolListHandler, MyResumeHandler, UpdateCompleteHandler, UploadURLHandler
from SignupCountHandler import SignupCountHandler
from ApplyCountHandler import ApplyCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
from AdminHandler import AdminHandler, ApproveResumeHandler, ApproveHandler
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
    ('/apply/uploadurl', UploadURLHandler),
    ('/applycount', ApplyCountHandler),
    ('/rules', RulesHandler),
    ('/schedule', ScheduleHandler),
    ('/signupcount', SignupCountHandler),
    ('/travel', TravelHandler),
    ('/tropo', TropoHandler),
    ('/admin', AdminHandler),
    ('/admin/approve', ApproveHandler),
    ('/admin/approve/resume/.*', ApproveResumeHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/_ah/login_required', LoginRequiredHandler),
    # ('/admin', AdminHandler.AdminHandler),
    ('.*', ErrorHandler)
]
