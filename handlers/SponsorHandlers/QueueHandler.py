import MainSponsorHandler
from db import constants
import json
from db.Task import Task

class QueueHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        tasks = []
        for t in self.db_user.task_queue:
            task = t.get()
            tasks.append({
                'complete':task.complete,
                'id':task.key.id(),
                'url':'http://23.236.61.209/serve/' + str(task.key.id()),
                'creationTime':task.creationTime.strftime('%x %X'),
                'completeTime':task.completeTime.strftime('%x %X'),
                'errorMessages':task.errorMessages,
            })
        return self.render('sponsor/queue.html', tasks=tasks, access=json.loads(self.db_user.access))
