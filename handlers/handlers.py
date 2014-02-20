from EmailBackupHandler import EmailBackupHandler
from ErrorHandlers import handle_401, handle_404, handle_500, Error401Handler, Error404Handler, Error500Handler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, SchoolCheckHandler, SchoolListHandler, MyResumeHandler, UpdateCompleteHandler, UploadURLHandler
from SignupCountHandler import SignupCountHandler
from ApplyCountHandler import ApplyCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
from AdminHandler import AdminApproveHandler, AdminResumeHandler, AdminStatsHandler
from SponsorHandler import SponsorHandler
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
    ('/admin/approve', AdminApproveHandler),
    ('/admin/stats', AdminStatsHandler),
    ('/admin/resume', AdminResumeHandler),
    ('/sponsor/download', SponsorHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/_ah/login_required', LoginRequiredHandler),
    # ('/admin', AdminHandler.AdminHandler),
	('/401', Error401Handler),
	('/404', Error404Handler),
	('/500', Error500Handler),
]
