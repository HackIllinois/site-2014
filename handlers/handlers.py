from webapp2_extras.routes import RedirectRoute

from EmailBackupHandler import EmailBackupHandler
from ErrorHandlers import handle_401, handle_404, handle_500, Error401Handler, Error404Handler, Error500Handler
from IndexHandler import IndexHandler
from ApplyHandler import ApplyHandler, ApplyCompleteHandler, SchoolCheckHandler, SchoolListHandler, MyResumeHandler, UpdateCompleteHandler, UploadURLHandler
from ApplyCountHandler import ApplyCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler, StaffHandler, SponsorFAQHandler
from TropoHandler import TropoHandler
from AdminHandler import AdminHandler, AdminApproveHandler, AdminResumeHandler, AdminStatsHandler, AdminBasicStatsHandler, AdminXkcdHandler, AdminProfileHandler, AdminEditProfileHandler, AdminApplyCountHandler, AdminSchoolCountHandler
from SponsorHandler import SponsorHandler
from LogoutHandler import LogoutHandler

handlers = [
    RedirectRoute('/', handler=IndexHandler, name='Index', strict_slash=True),
    RedirectRoute('/emailbackup', handler=EmailBackupHandler, name='EmailBackup', strict_slash=True),

    RedirectRoute('/apply', handler=ApplyHandler, name='Apply', strict_slash=True),
    RedirectRoute('/apply/complete', handler=ApplyCompleteHandler, name='ApplyComplete', strict_slash=True),
    RedirectRoute('/apply/updated', handler=UpdateCompleteHandler, name='UpdateComplete', strict_slash=True),
    RedirectRoute('/apply/schoolcheck', handler=SchoolCheckHandler, name='SchoolCheck', strict_slash=True),
    RedirectRoute('/apply/schoollist', handler=SchoolListHandler, name='SchoolList', strict_slash=True),
    RedirectRoute('/apply/myresume', handler=MyResumeHandler, name='MyResume', strict_slash=True),
    RedirectRoute('/apply/uploadurl', handler=UploadURLHandler, name='UploadURL', strict_slash=True),
    RedirectRoute('/applycount', handler=ApplyCountHandler, name='ApplyCount', strict_slash=True),

    RedirectRoute('/rules', handler=RulesHandler, name='Rules', strict_slash=True),
    RedirectRoute('/schedule', handler=ScheduleHandler, name='Schedule', strict_slash=True),
    RedirectRoute('/travel', handler=TravelHandler, name='Travel', strict_slash=True),
    RedirectRoute('/sponsor/faq', handler=SponsorFAQHandler, name='SponsorFAQ', strict_slash=True),
    RedirectRoute('/tropo', handler=TropoHandler, name='Tropo', strict_slash=True),
    RedirectRoute('/code-of-conduct', handler=CoCHandler, name='CoC', strict_slash=True),

    RedirectRoute('/sponsor/download', handler=SponsorHandler, name='Sponsor', strict_slash=True),

    RedirectRoute('/admin', handler=AdminHandler, name='Admin', strict_slash=True),
    RedirectRoute('/admin/xkcd', handler=AdminXkcdHandler, name='AdminXkcd', strict_slash=True),
    RedirectRoute('/admin/approve', handler=AdminApproveHandler, name='AdminApprove', strict_slash=True),
    RedirectRoute('/admin/stats', handler=AdminStatsHandler, name='AdminStats', strict_slash=True),
    RedirectRoute('/admin/basicstats', handler=AdminBasicStatsHandler, name='AdminBasicStats', strict_slash=True),
    RedirectRoute('/admin/resume', handler=AdminResumeHandler, name='AdminResume', strict_slash=True),
    RedirectRoute('/admin/applycount', handler=AdminApplyCountHandler, name='AdminApplyCount', strict_slash=True),
    RedirectRoute('/admin/schoolcount', handler=AdminSchoolCountHandler, name='AdminSchoolCount', strict_slash=True),
    RedirectRoute('/admin/profile/<userId>', handler=AdminProfileHandler, name='AdminProfile', strict_slash=True),
    RedirectRoute('/admin/profile/<userId>/edit', handler=AdminEditProfileHandler, name='AdminEditProfile', strict_slash=True),

    RedirectRoute('/logout', handler=LogoutHandler, name='Logout', strict_slash=True),

    # RedirectRoute('/hidden/staff', handler=StaffHandler, name='Staff', strict_slash=True),
    RedirectRoute('/mgt', handler=MGTHandler, name='MGT', strict_slash=True),
    RedirectRoute('/particles', handler=ParticlesHandler, name='Particles', strict_slash=True),

    RedirectRoute('/401', handler=Error401Handler, name='Error401', strict_slash=True),
    RedirectRoute('/404', handler=Error404Handler, name='Error404', strict_slash=True),
    RedirectRoute('/500', handler=Error500Handler, name='Error500', strict_slash=True),
]

errorHandlers = {
    401: handle_401,
    404: handle_404,
    500: handle_500,
}
