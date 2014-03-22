from webapp2_extras.routes import RedirectRoute

from EmailBackupHandler import EmailBackupHandler
from IndexHandler import IndexHandler
from ApplyCountHandler import ApplyCountHandler
from TropoHandler import TropoHandler
from SponsorHandler import SponsorDownloadHandler
from LogoutHandler import LogoutHandler
from MGTHandler import MGTHandler, ParticlesHandler
from TestAllHandler import TestAllHandler, TestAllJsHandler
import ApplyHandler
import MentorHandler
import SkillsHandler
import SubpageHandlers
import AdminHandler
import MobileHandler
import ErrorHandlers

handlers = [
    RedirectRoute('/', handler=IndexHandler, name='Index', strict_slash=True),
    RedirectRoute('/emailbackup', handler=EmailBackupHandler, name='EmailBackup', strict_slash=True),

    RedirectRoute('/apply', handler=ApplyHandler.ApplyHandler, name='Apply', strict_slash=True),
    RedirectRoute('/apply/update', handler=ApplyHandler.ApplyHandler, name='ApplyUpdate', strict_slash=True),
    RedirectRoute('/apply/complete', handler=ApplyHandler.ApplyCompleteHandler, name='ApplyComplete', strict_slash=True),
    RedirectRoute('/apply/updated', handler=ApplyHandler.UpdateCompleteHandler, name='UpdateComplete', strict_slash=True),
    RedirectRoute('/apply/schoolcheck', handler=ApplyHandler.SchoolCheckHandler, name='SchoolCheck', strict_slash=True),
    RedirectRoute('/apply/schoollist', handler=ApplyHandler.SchoolListHandler, name='SchoolList', strict_slash=True),
    RedirectRoute('/apply/myresume', handler=ApplyHandler.MyResumeHandler, name='MyResume', strict_slash=True),
    RedirectRoute('/apply/uploadurl', handler=ApplyHandler.UploadURLHandler, name='UploadURL', strict_slash=True),

    RedirectRoute('/applycount', handler=ApplyCountHandler, name='ApplyCount', strict_slash=True),

    RedirectRoute('/rules', handler=SubpageHandlers.RulesHandler, name='Rules', strict_slash=True),
    RedirectRoute('/schedule', handler=SubpageHandlers.ScheduleHandler, name='Schedule', strict_slash=True),
    RedirectRoute('/travel', handler=SubpageHandlers.TravelHandler, name='Travel', strict_slash=True),
    RedirectRoute('/sponsor/faq', handler=SubpageHandlers.SponsorFAQHandler, name='SponsorFAQ', strict_slash=True),
    RedirectRoute('/code-of-conduct', handler=SubpageHandlers.CoCHandler, name='CoC', strict_slash=True),

    RedirectRoute('/tropo', handler=TropoHandler, name='Tropo', strict_slash=True),

    RedirectRoute('/sponsor/download', handler=SponsorDownloadHandler, name='SponsorDownload', strict_slash=True),

    RedirectRoute('/admin', handler=AdminHandler.AdminHandler, name='Admin', strict_slash=True),
    RedirectRoute('/admin/xkcd', handler=AdminHandler.AdminXkcdHandler, name='AdminXkcd', strict_slash=True),
    RedirectRoute('/admin/approve', handler=AdminHandler.AdminApproveHandler, name='AdminApprove', strict_slash=True),
    RedirectRoute('/admin/stats', handler=AdminHandler.AdminStatsHandler, name='AdminStats', strict_slash=True),
    RedirectRoute('/admin/basicstats', handler=AdminHandler.AdminBasicStatsHandler, name='AdminBasicStats', strict_slash=True),
    RedirectRoute('/admin/resume', handler=AdminHandler.AdminResumeHandler, name='AdminResume', strict_slash=True),
    RedirectRoute('/admin/applycount', handler=AdminHandler.AdminApplyCountHandler, name='AdminApplyCount', strict_slash=True),
    RedirectRoute('/admin/schoolcount', handler=AdminHandler.AdminSchoolCountHandler, name='AdminSchoolCount', strict_slash=True),
    RedirectRoute('/admin/profile/<userId>', handler=AdminHandler.AdminProfileHandler, name='AdminProfile', strict_slash=True),
    RedirectRoute('/admin/profile/<userId>/edit', handler=AdminHandler.AdminEditProfileHandler, name='AdminEditProfile', strict_slash=True),
    RedirectRoute('/admin/manager', handler=AdminHandler.AdminManagerHandler, name='AdminManager', strict_slash=True),
    RedirectRoute('/admin/manager/accesscontrol', handler=AdminHandler.AdminAccessControlHandler, name='AdminAccessControl', strict_slash=True),
    RedirectRoute('/admin/export', handler=AdminHandler.AdminExportHandler, name='AdminExport', strict_slash=True),
    # RedirectRoute('/admin/mentors', handler=AdminHandler.AdminMentorsHandler, name='AdminMentors', strict_slash=True),
    # RedirectRoute('/admin/skills', handler=AdminHandler.AdminSkillsHandler, name='AdminSkills', strict_slash=True),

    RedirectRoute('/admin/tests', handler=TestAllHandler, name='TestAll', strict_slash=True),
    RedirectRoute('/admin/testsjs', handler=TestAllJsHandler, name='TestAllJs', strict_slash=True),

    RedirectRoute('/mobile/schedule', handler=MobileHandler.ScheduleHandler, name='MobileSchedule', strict_slash=True),
    RedirectRoute('/mobile/support', handler=MobileHandler.SupportHandler, name='MobileSupportType', strict_slash=True),
    RedirectRoute('/mobile/newsfeed', handler=MobileHandler.NewsfeedHandler, name='MobileNewsfeed', strict_slash=True),
    RedirectRoute('/mobile/person', handler=MobileHandler.PersonHandler, name='MobileHacker', strict_slash=True),
    RedirectRoute('/mobile/skills', handler=MobileHandler.SkillsHandler, name='MobileSkills', strict_slash=True),
    RedirectRoute('/mobile/login', handler=MobileHandler.LoginHandler, name='MobileLogin', strict_slash=True),

    RedirectRoute('/logout', handler=LogoutHandler, name='Logout', strict_slash=True),

    # RedirectRoute('/hidden/staff', handler=SubpageHandlers.StaffHandler, name='Staff', strict_slash=True),
    RedirectRoute('/mgt', handler=MGTHandler, name='MGT', strict_slash=True),
    RedirectRoute('/particles', handler=ParticlesHandler, name='Particles', strict_slash=True),

    RedirectRoute('/401', handler=ErrorHandlers.Error401Handler, name='Error401', strict_slash=True),
    RedirectRoute('/404', handler=ErrorHandlers.Error404Handler, name='Error404', strict_slash=True),
    RedirectRoute('/500', handler=ErrorHandlers.Error500Handler, name='Error500', strict_slash=True),
]

errorHandlers = {
    401: ErrorHandlers.handle_401,
    404: ErrorHandlers.handle_404,
    500: ErrorHandlers.handle_500,
}
