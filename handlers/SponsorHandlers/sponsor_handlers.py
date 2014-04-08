from webapp2_extras.routes import RedirectRoute

import IndexHandler
import EditProfileHandler
import SupportHandler
import HackersHandler
import QueueHandler
import SimpleHandlers
import ExportHandler

import RegistrationHandler
import RegisterHandler

sponsor_handlers = [
    RedirectRoute('/corporate',                 handler=IndexHandler.IndexHandler,              name='SponsorIndex',            strict_slash=True),
    RedirectRoute('/corporate/editprofile',     handler=EditProfileHandler.EditProfileHandler,  name='SponsorEditProfile',      strict_slash=True),
    RedirectRoute('/corporate/support',         handler=SupportHandler.SupportHandler,          name='SponsorSupport',          strict_slash=True),

    RedirectRoute('/corporate/hackers',         handler=HackersHandler.HackersHandler,          name='SponsorHackers',          strict_slash=True),
    RedirectRoute('/corporate/hackers/<key>',   handler=HackersHandler.HackersHandler,          name='SponsorHackersProfile',   strict_slash=True),

    RedirectRoute('/corporate/queue',           handler=QueueHandler.QueueHandler,              name='SponsorQueue',            strict_slash=True),
    RedirectRoute('/corporate/notregistered',   handler=SimpleHandlers.NotRegisteredHandler,    name='SponsorNotRegistered',    strict_slash=True),

    # Not a /corporate url on purpose
    RedirectRoute('/c-registration/<key>',      handler=RegistrationHandler.RegistrationHandler, name='SponsorRegistration',    strict_slash=True),

    RedirectRoute('/corporate/register/<key>',  handler=RegisterHandler.RegisterHandler,        name='SponsorRegister',         strict_slash=True),
]
