from EmailBackupHandler import EmailBackupHandler
from ErrorHandlers import handle_401, handle_404, handle_500, Error401Handler, Error404Handler, Error500Handler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, SchoolCheckHandler, SchoolListHandler, MyResumeHandler, UpdateCompleteHandler, UploadURLHandler
from SignupCountHandler import SignupCountHandler
from ApplyCountHandler import ApplyCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
from AdminHandler import AdminHandler, AdminApproveHandler, AdminResumeHandler, AdminStatsHandler, AdminBasicStatsHandler, AdminXkcdHandler, AdminApplyCountHandler, AdminSchoolCountHandler
from SponsorHandler import SponsorHandler
from LogoutHandler import LogoutHandler


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
    ('/admin/xkcd', AdminXkcdHandler),
    ('/admin/approve', AdminApproveHandler),
    ('/admin/stats', AdminStatsHandler),
    ('/admin/basicstats', AdminBasicStatsHandler),
    ('/admin/resume', AdminResumeHandler),
    ('/admin/applycount', AdminApplyCountHandler),
    ('/admin/schoolcount', AdminSchoolCountHandler),
    ('/sponsor/download', SponsorHandler),
    ('/code-of-conduct', CoCHandler),
    ('/logout', LogoutHandler),
	('/401', Error401Handler),
	('/404', Error404Handler),
	('/500', Error500Handler),
]

errorHandlers = {
    401: handle_401,
    404: handle_404,
    500: handle_500,
}
