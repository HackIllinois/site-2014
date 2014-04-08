import MainSponsorHandler
from db import constants
import json
from db.Task import Task
from operator import itemgetter

class QueueHandler(MainSponsorHandler.BaseSponsorHandler):
    def get(self):
        tasks = []
        for t in self.db_user.task_queue:
            task = t.get()
            if not task: continue

            errors = task.errorMessages
            if errors:
                errors = errors[1:]
                errors = errors[:-1]
                if len(errors) > 50: errors = errors[:50] + '...'

            tasks.append({
                'complete':task.complete,
                'id':task.key.id(),
                'url':'http://23.236.61.209/serve/HackIllinois-' + str(task.key.id()) + '.zip',
                'creationTime':task.creationTime.strftime('%x %X'),
                'completeTime':task.completeTime.strftime('%x %X') if task.completeTime else '',
                'errorMessages':errors if errors else '',
                'sort':task.creationTime,
            })

        tasks = sorted(tasks, key=itemgetter('sort'), reverse=True)

        return self.render('sponsor/queue.html', tasks=tasks, access=json.loads(self.db_user.access))
