from EmailBackupHandler import EmailBackupHandler
from ErrorHandler import ErrorHandler
from IndexHandler import IndexHandler
from RegisterHandler import RegisterHandler, RegisterCompleteHandler, SchoolCheckHandler
from SignupCountHandler import SignupCountHandler
from SubpageHandlers import RulesHandler, ScheduleHandler, TravelHandler, CoCHandler
from TropoHandler import TropoHandler
<<<<<<< HEAD
from AdminHandler import AdminHandler
from ApproveHandler import ApproveHandler
import ProfileHandler
=======
from ProfileHandler import ProfileHandler, MyResumeHandler
>>>>>>> ef69ad9a0b1bd66fe4248e86e34eb227dc70402b
# import AdminHandler
# from LoginRequiredHandler import LoginRequiredHandler


handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('/register', RegisterHandler),
    ('/register/complete', RegisterCompleteHandler),
    ('/register/schoolcheck', SchoolCheckHandler),
    ('/rules', RulesHandler),
    ('/schedule', ScheduleHandler),
    ('/signupcount', SignupCountHandler),
    ('/travel', TravelHandler),
    ('/tropo', TropoHandler),
<<<<<<< HEAD
    ('/profile', ProfileHandler.ProfileHandler),
    ('/admin', AdminHandler),
    ('/admin/approve', ApproveHandler),
=======
    ('/profile', ProfileHandler),
    ('/profile/myresume', MyResumeHandler),
    ('/code-of-conduct', CoCHandler),
    # ('/admin', AdminHandler.AdminHandler),
>>>>>>> ef69ad9a0b1bd66fe4248e86e34eb227dc70402b
    # ('/_ah/login_required', LoginRequiredHandler),
    ('.*', ErrorHandler)
]
