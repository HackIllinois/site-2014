import MainHandler
import db.models as models

class ApproveHandler(MainHandler.Handler):

    def get(self):
        ## @TODO: login implementation

        db_all_users = models.search_database(models.Attendee, {})
        if db_all_users is None:
            return self.response.out.write('ERROR') # @TODO: implement error handling here

        results = db_all_users.fetch(10)
        print len(results)
        
        for d in results:
            print 'hi'
            print d.nameFirst

        self.render('approve.html')