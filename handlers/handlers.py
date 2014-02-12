from EmailBackupHandler import EmailBackupHandler
from ErrorHandler import ErrorHandler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, SchoolCheckHandler, SchoolListHandler, MyResumeHandler, UpdateCompleteHandler, UploadURLHandler
from SignupCountHandler import SignupCountHandler
from ApplyCountHandler import ApplyCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
from AdminHandler import SummaryHandler, AdminResumeHandler
# from AdminHandler import AdminHandler, ApproveResumeHandler, ApproveHandler
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
    # I may have broken all of this code with the backend refactor, will help get it fixed soon. --Matthew
    # ('/admin', AdminHandler),
    # ('/admin/approve', ApproveHandler),
    # ('/admin/approve/resume/.*', ApproveResumeHandler),
    ('/admin', SummaryHandler),
    ('/admin/resume', AdminResumeHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/_ah/login_required', LoginRequiredHandler),
    # ('/admin', AdminHandler.AdminHandler),
    ('.*', ErrorHandler)
]
