from webapp2_extras.routes import RedirectRoute

from EmailBackupHandler import EmailBackupHandler
from IndexHandler import IndexHandler
from ApplyCountHandler import ApplyCountHandler
from TropoHandler import TropoHandler
from SponsorHandler import SponsorDownloadHandler
from LogoutHandler import LogoutHandler
from MGTHandler import MGTHandler, ParticlesHandler
from RsvpHandler import RsvpHandler, NotApprovedHandler, RsvpYesHandler, RsvpNoHandler, RsvpClosedHandler
import ApplyHandler
import MentorHandler
import SubpageHandlers
import AdminHandlers
import MobileHandler
import ErrorHandlers

handlers = [
    RedirectRoute('/', handler=IndexHandler, name='Index', strict_slash=True),
    RedirectRoute('/emailbackup', handler=EmailBackupHandler, name='EmailBackup', strict_slash=True),

    RedirectRoute('/apply', handler=ApplyHandler.ApplyHandler, name='Apply', strict_slash=True),
    RedirectRoute('/apply/update', handler=ApplyHandler.ApplyHandler, name='ApplyUpdate', strict_slash=True),
    RedirectRoute('/apply/whitelist/<unique_string>', handler=ApplyHandler.ApplyHandler, name='ApplyWhitelist', strict_slash=True),

    RedirectRoute('/apply/complete', handler=ApplyHandler.ApplyCompleteHandler, name='ApplyComplete', strict_slash=True),
    RedirectRoute('/apply/closed', handler=ApplyHandler.ApplicationsClosedHandler, name='ApplicationsClosed', strict_slash=True),
    RedirectRoute('/apply/updated', handler=ApplyHandler.UpdateCompleteHandler, name='UpdateComplete', strict_slash=True),
    RedirectRoute('/apply/schoolcheck', handler=ApplyHandler.SchoolCheckHandler, name='SchoolCheck', strict_slash=True),
    RedirectRoute('/apply/schoollist', handler=ApplyHandler.SchoolListHandler, name='SchoolList', strict_slash=True),
    RedirectRoute('/apply/myresume', handler=ApplyHandler.MyResumeHandler, name='MyResume', strict_slash=True),
    RedirectRoute('/apply/uploadurl', handler=ApplyHandler.UploadURLHandler, name='UploadURL', strict_slash=True),

    RedirectRoute('/rsvp', handler=RsvpHandler, name='Rsvp', strict_slash=True),
    RedirectRoute('/rsvp/pending', handler=NotApprovedHandler, name='RsvpNotApproved', strict_slash=True),
    RedirectRoute('/rsvp/yes', handler=RsvpYesHandler, name='RsvpYes', strict_slash=True),
    RedirectRoute('/rsvp/no', handler=RsvpNoHandler, name='RsvpNo', strict_slash=True),
    RedirectRoute('/rsvp/closed', handler=RsvpClosedHandler, name='RsvpClosed', strict_slash=True),

    RedirectRoute('/mentor', handler=MentorHandler.RenderHandler, name='Mentor', strict_slash=True),

    RedirectRoute('/applycount', handler=ApplyCountHandler, name='ApplyCount', strict_slash=True),

    RedirectRoute('/rules', handler=SubpageHandlers.RulesHandler, name='Rules', strict_slash=True),
    RedirectRoute('/schedule', handler=SubpageHandlers.ScheduleHandler, name='Schedule', strict_slash=True),
    RedirectRoute('/travel', handler=SubpageHandlers.TravelHandler, name='Travel', strict_slash=True),
    RedirectRoute('/sponsor/faq', handler=SubpageHandlers.SponsorFAQHandler, name='SponsorFAQ', strict_slash=True),
    RedirectRoute('/code-of-conduct', handler=SubpageHandlers.CoCHandler, name='CoC', strict_slash=True),

    RedirectRoute('/tropo', handler=TropoHandler, name='Tropo', strict_slash=True),

    RedirectRoute('/sponsor/download', handler=SponsorDownloadHandler, name='SponsorDownload', strict_slash=True),

    # If you create a new file in AdminHandlers, make sure to add it to AdminHandlers/__init__.py
    RedirectRoute('/admin', handler=AdminHandlers.IndexHandler.IndexHandler, name='AdminIndex', strict_slash=True),
    RedirectRoute('/admin/xkcd', handler=AdminHandlers.XkcdHandler.XkcdHandler, name='AdminXkcd', strict_slash=True),
    RedirectRoute('/admin/stats', handler=AdminHandlers.StatsHandler.StatsHandler, name='AdminStats', strict_slash=True),
    RedirectRoute('/admin/rsvpstats', handler=AdminHandlers.RsvpStatsHandler.RsvpStatsHandler, name='AdminRsvpStats', strict_slash=True),
    RedirectRoute('/admin/busstats', handler=AdminHandlers.BusRouteStatsHandler.BusRouteStatsHandler, name='AdminBusStats', strict_slash=True),
    RedirectRoute('/admin/resume', handler=AdminHandlers.ResumeHandler.ResumeHandler, name='AdminResume', strict_slash=True),
    RedirectRoute('/admin/applycount', handler=AdminHandlers.ApplyCountHandler.ApplyCountHandler, name='AdminApplyCount', strict_slash=True),
    RedirectRoute('/admin/schoolcount', handler=AdminHandlers.SchoolCountHandler.SchoolCountHandler, name='AdminSchoolCount', strict_slash=True),
    RedirectRoute('/admin/profile/<userId>', handler=AdminHandlers.ProfileHandler.ProfileHandler, name='AdminProfile', strict_slash=True),
    RedirectRoute('/admin/manager', handler=AdminHandlers.ManagerHandler.ManagerHandler, name='AdminManager', strict_slash=True),
    RedirectRoute('/admin/manager/accesscontrol', handler=AdminHandlers.AccessControlHandler.AccessControlHandler, name='AdminAccessControl', strict_slash=True),
    RedirectRoute('/admin/manager/whitelistcontrol', handler=AdminHandlers.ManagerHandler.WhitelistControlHandler, name='AdminWhitelistControl', strict_slash=True),
    RedirectRoute('/admin/send', handler=AdminHandlers.MarkSentEmailHandler.MarkSentEmailHandler, name='AdminMarkSentEmail', strict_slash=True),
    RedirectRoute('/admin/massapproval', handler=AdminHandlers.MassApprovalHandler.MassApprovalHandler, name='AdminMassApproval', strict_slash=True),

    RedirectRoute('/admin/basicstats',          handler=AdminHandlers.BasicStatsHandler.BasicStatsHandler, name='AdminBasicStats0', strict_slash=True),
    RedirectRoute('/admin/basicstats/<status>', handler=AdminHandlers.BasicStatsHandler.BasicStatsHandler, name='AdminBasicStats1', strict_slash=True),

    RedirectRoute('/admin/export',                             handler=AdminHandlers.ExportHandler.ExportHandler, name='AdminExport0', strict_slash=True),
    RedirectRoute('/admin/export/<status>',                    handler=AdminHandlers.ExportHandler.ExportHandler, name='AdminExport1', strict_slash=True),
    RedirectRoute('/admin/export/<status>/<category>',         handler=AdminHandlers.ExportHandler.ExportHandler, name='AdminExport2', strict_slash=True),
    RedirectRoute('/admin/export/<status>/<category>/<route>', handler=AdminHandlers.ExportHandler.ExportHandler, name='AdminExport3', strict_slash=True),

    RedirectRoute('/admin/approve',                             handler=AdminHandlers.ApproveHandlers.ApproveHandler, name='AdminApprove0', strict_slash=True),
    RedirectRoute('/admin/approve/<status>',                    handler=AdminHandlers.ApproveHandlers.ApproveHandler, name='AdminApprove1', strict_slash=True),
    RedirectRoute('/admin/approve/<status>/<category>',         handler=AdminHandlers.ApproveHandlers.ApproveHandler, name='AdminApprove2', strict_slash=True),
    RedirectRoute('/admin/approve/<status>/<category>/<route>', handler=AdminHandlers.ApproveHandlers.ApproveHandler, name='AdminApprove3', strict_slash=True),

    RedirectRoute('/admin/rsvp',                             handler=AdminHandlers.RsvpHandler.RsvpHandler, name='AdminRsvp0', strict_slash=True),
    RedirectRoute('/admin/rsvp/<status>',                    handler=AdminHandlers.RsvpHandler.RsvpHandler, name='AdminRsvp1', strict_slash=True),
    RedirectRoute('/admin/rsvp/<status>/<category>',         handler=AdminHandlers.RsvpHandler.RsvpHandler, name='AdminRsvp2', strict_slash=True),
    RedirectRoute('/admin/rsvp/<status>/<category>/<route>', handler=AdminHandlers.RsvpHandler.RsvpHandler, name='AdminRsvp3', strict_slash=True),

    RedirectRoute('/admin/tests', handler=AdminHandlers.TestAllHandler.TestAllHandler, name='TestAll', strict_slash=True),
    RedirectRoute('/admin/testsjs', handler=AdminHandlers.TestAllHandler.TestAllJsHandler, name='TestAllJs', strict_slash=True),

    RedirectRoute('/admin/skills', handler=AdminHandlers.AddingSkillsHandler.AddingSkillsHandler, name='AdminSkills', strict_slash=True),
    # RedirectRoute('/admin/updateschema', handler=AdminHandlers.UpdateSchemaHandler.UpdateSchemaHandler, name='UpdateSchema', strict_slash=True),

    RedirectRoute('/mobile/schedule', handler=MobileHandler.ScheduleHandler, name='MobileSchedule', strict_slash=True),
    RedirectRoute('/mobile/map', handler=MobileHandler.MapHandler, name='MobileMap', strict_slash=True),
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
