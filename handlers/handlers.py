from IndexHandler import IndexHandler
from EmailBackupHandler import EmailBackupHandler
from RegisterHandler import RegisterHandler
from ErrorHandler import ErrorHandler
from TropoHandler import TropoHandler

handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('/register', RegisterHandler),
    ('/tropo', TropoHandler),
    ('.*', ErrorHandler)
]
