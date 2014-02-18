from EmailBackupHandler import EmailBackupHandler
from ErrorHandlers import handle_401, handle_404, handle_500, Error401Handler, Error404Handler, Error500Handler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, SchoolCheckHandler, SchoolListHandler, MyResumeHandler, UpdateCompleteHandler, UploadURLHandler
from ApplyCountHandler import ApplyCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler, StaffHandler, SponsorFAQHandler
from TropoHandler import TropoHandler
<<<<<<< HEAD
from AdminHandler import AdminHandler, AdminApproveHandler, AdminResumeHandler, AdminStatsHandler, AdminBasicStatsHandler, AdminXkcdHandler, AdminApplyCountHandler, AdminSchoolCountHandler
from SponsorHandler import SponsorHandler
from LogoutHandler import LogoutHandler
from MGTHandler import MGTHandler, ParticlesHandler
=======
from AdminHandler import SummaryHandler, AdminResumeHandler, AdminStatsHandler
from MobileHandler import MobileHandler, ScheduleHandler, MapsHandler, SupportTypeHandler, EmergencyHandler, NewsfeedHandler, StaffHandler, HackersHandler, CompanyHandler, SkillsHandler
# from AdminHandler import AdminHandler, ApproveResumeHandler, ApproveHandler
# import AdminHandler
# from LoginRequiredHandler import LoginRequiredHandler
>>>>>>> setup endpoints in handlers and basic outline in MobileHandlers


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
    ('/travel', TravelHandler),
    ('/sponsor/faq', SponsorFAQHandler),
    ('/tropo', TropoHandler),
    ('/admin', AdminHandler),
    ('/admin/xkcd', AdminXkcdHandler),
    ('/admin/approve', AdminApproveHandler),
#    ('/mobile', )
#    ('/mobile', MobileLoginHandler)
    ('/mobile', MobileLoginHandler),
#    ('/mobile/schedule', ScheduleHandler)
#    ('/mobile/maps', MapsHandler)
#    ('/mobile/support/types', SupportTypeHandler)
#    ('/mobile/messages/emergency', EmergencyHandler)
#    ('/mobile/messages/newsfeed', NewsfeedHandler)
#    ('/mobile/people/staff, StaffHandler)
#    ('/mobile/people/hackers', HackersHandler)
#    ('/mobile/company', CompanyHandler)
#    ('/mobile/skills', SkillsHandler)
    # I may have broken all of this code with the backend refactor, will help get it fixed soon. --Matthew
    # ('/admin', AdminHandler),
    # ('/admin/approve', ApproveHandler),
    # ('/admin/approve/resume/.*', ApproveResumeHandler),
    ('/admin', SummaryHandler),
    ('/admin/resume', AdminResumeHandler),
    ('/admin/stats', AdminStatsHandler),
    ('/admin/basicstats', AdminBasicStatsHandler),
    ('/admin/resume', AdminResumeHandler),
    ('/admin/applycount', AdminApplyCountHandler),
    ('/admin/schoolcount', AdminSchoolCountHandler),
    ('/sponsor/download', SponsorHandler),    
    ('/code-of-conduct', CoCHandler),
    # ('/hidden/staff', StaffHandler),
    ('/logout', LogoutHandler),
    ('/mgt', MGTHandler),
    ('/particles', ParticlesHandler),
	('/401', Error401Handler),
	('/404', Error404Handler),
	('/500', Error500Handler),
]

errorHandlers = {
    401: handle_401,
    404: handle_404,
    500: handle_500,
}
