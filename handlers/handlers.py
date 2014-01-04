from IndexHandler import IndexHandler
from EmailBackupHandler import EmailBackupHandler
from RegisterHandler import RegisterHandler
from ErrorHandler import ErrorHandler

handlers = [
    ('/', IndexHandler),
    ('/emailbackup', EmailBackupHandler),
    ('/register', RegisterHandler),
    ('.*', ErrorHandler)
]
