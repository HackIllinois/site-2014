import cgi
import MainHandler
import operator
from collections import Counter
from db.models import SignUp

class SignupCountHandler(MainHandler.Handler):
    """ Handler for a quick page to count the number of email signups we have """
    def get(self):
        aliases = {
            'illinois.edu': ['uiuc.edu','acm.uiuc.edu'],
            'gmail.com': ['googlemail.com'],
        }
        q = SignUp.query()
        domains = []
        only_edu = 'onlyEdu' in self.request.query_string
        for signup in q.iter():
            domain = signup.email.split('@',1)[1].lower()
            if only_edu and not domain.endswith('.edu'):
                continue
            domains.append(domain)
        c = Counter(domains)
        for key in aliases:
            if key not in c:
                continue
            for alias in aliases[key]:
                c[key] += c[alias]
                del c[alias]
        sorted_counts = sorted(c.iteritems(), key=operator.itemgetter(1), reverse=True)
        self.write("<ul>")
        for counts in sorted_counts:
            self.write("<li>" + counts[0] + ": " + str(counts[1]) + "</li>")
        self.write("</ul>")
