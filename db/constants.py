ADMIN_EMAILS = set(['lx.icomputer@gmail.com','mvd7793@gmail.com','austin.1111h@gmail.com','fishben2@illinois.edu','jacob@hackillinois.org'])

BUCKET = 'hackillinois'

MEMCACHE_TIMEOUT = 10800 # seconds = 3 hours , once we close registration increase to 1 day
MOBILE_MEMCACHE_TIMEOUT = 86400 # second = 1 day (24 hours)
MEMCACHE_COUNT_TIMEOUT = 900 # seconds = 15 min
USE_ADMIN_MEMCACHE = False

APPLY_TITLE = 'Application'
PROFILE_TITLE = 'Profile'
RSVP_TITLE = 'RSVP'

APPLY_COMPLETE_HEADER = 'Application Complete!'
APPLY_COMPLETE_MESSAGE = 'Thanks for applying! To keep in touch, follow us on Facebook and Twitter. Also, don\'t forget to RSVP to the <a href="http://go.hackillinois.org/event" target="_blank" style="color: #ef3e36">Facebook event</a>!'

UPDATE_COMPLETE_HEADER = 'Application Updated!'
UPDATE_COMPLETE_MESSAGE = 'Thanks for updating your application!<br>To keep in touch, follow us on Facebook and Twitter.<br>Also, don\'t forget to RSVP to the <a href="http://go.hackillinois.org/event" target="_blank" style="color: #ef3e36">Facebook event</a>!'

APPLICATION_CLOSED_HEADER = 'Applications Are Closed'
APPLICATION_CLOSED_MESSAGE = 'We\'re sorry, but applications for HackIllinois closed on March 21st.<br>Please try again next time, and happy hacking!<br><br>If you have already registered, please <a href="/logout?redirect=/apply/update" style="color: #ef3e36">logout</a> and login with the account you used to register.'

NOT_APPROVED_HEADER = 'Application Pending Review'
NOT_APPROVED_MESSAGE = 'Your application is still being reviewed by our staff.<br>You will receive an email once your application has been reviewed.'

RSVP_YES_HEADER = 'RSVP Complete!'
RSVP_YES_MESSAGE = 'Thanks for RSVPing, and welcome to HackIllinois!<br>To keep in touch, follow us on Facebook and Twitter, RSVP to the <a href="http://go.hackillinois.org/event" target="_blank" style="color: #ef3e36">Facebook event</a>,<br>and join your school\'s <a href="http://go.hackillinois.org/fbgroups" target="_blank" style="color: #ef3e36">Facebook group</a> to meet other hackers from your school.'

RSVP_NO_HEADER = 'RSVP Complete.'
RSVP_NO_MESSAGE = 'Thanks for RSVPing! We are sorry that you cannot make it.<br>To keep in touch for the next HackIllinois, follow us on Facebook and Twitter.'

RSVP_CLOSED_HEADER = 'RSVP Deadline Passed'
RSVP_CLOSED_MESSAGE = 'We\'re sorry, but your RSVP deadline for HackIllinois has past.<br>We have released your spot to another hacker on the waitlist.<br>Please apply again for the next HackIllinois. Happy hacking!'

ERROR_MESSAGE_PREFIX = 'Please provide '
ERROR_MESSAGE_SUFFIX = '.'

ALL_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'resume', 'linkedin', 'github', 'shirt', 'food', 'foodInfo', 'projectType', 'experience', 'termsOfService', 'travel']
REQUIRED_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'shirt', 'experience', 'travel']

# This should have *ALL* fields in REQUIRED_FIELDS *EXCEPT* for 'termsOfService'
READABLE_REQUIRED_FIELDS = {'nameFirst':'your first name',
                            'nameLast':'your last name',
                            'email':'your valid e-mail address',
                            'gender':'your gender',
                            'school':'your school',
                            'year':'your year in school',
                            'shirt':'your T-shirt size',
                            'experience':'your past experience',
                            'projectType':'your project type',
                            'travel':'your travel arrangements'}

READABLE_FIELDS = {'food':'your dietary restrictions',
                   'food-info':'your dietary restriction information'}

TOS_ERROR_MESSAGE = 'Please accept the Terms of Service'

CSV_HEADINGS = ['First Name','Last Name','Email',
                'Gender','School','Year','LinkedIn',
                'Github','Shirt','Food','Project Type',
                'Travel Preference', 'Bus Route',
                'Registration Time','Is Approved',
                'Previous Experience', 'Team Members',
                'User ID','Resume','Status']

# The below array is for more descriptive error messages. @Mattato pls fix.
# READABLE_REQUIRED_FIELDS = ['First Name','Last Name','E-mail','Gender','School','Year in School','T-shirt size','past experience', 'Please accept the Terms of Service']

EMAIL_MATCH = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$"

GENDERS = ['Male','Female','Other', 'I choose not to specify']
YEARS = ['Freshman','Sophomore','Junior','Senior','Grad','HS']
SHIRTS = ['XS','S','M','L','XL','XXL']
FOODS = ['Vegetarian','Vegan','Gluten Free','Lactose Free', 'Other']
PROJECTS = ['Software Hack','Hardware Hack','Unsure']

MICRO1 = [['Arduinos','http://www.arduino.cc/'],['Raspberry Pi','http://www.raspberrypi.org/']]
MICRO2 = [['Electric Imp Dev Kit','http://www.electricimp.com/'],['Spark Core','https://www.spark.io/']]
LABEQUIPMENT = ['Power Supplies','Oscilloscopes']

TRAVEL_RIDE_BUS = 'I would like to ride a HackIllinois bus'
TRAVEL_PROVIDE_OWN_TRANSIT = 'I will provide my own transportation'
TRAVEL_ALREADY_AT_UIUC = 'I am already in Urbana-Champaign, IL'
TRAVEL_NO_RESPONSE = 'I have not responded to this quesiton'
TRAVEL_ARRANGEMENTS = [TRAVEL_RIDE_BUS, TRAVEL_PROVIDE_OWN_TRANSIT, TRAVEL_ALREADY_AT_UIUC]

STATUSES = [
    'Not Approved',
    'Approved',
    'Waitlisted',
    'Awaiting Response',
    'Rsvp Coming',
    'Rsvp Not Coming',
    'No Rsvp'
]

APPROVE_STATUSES = [
    'Not Approved',
    'Approved',
    'Waitlisted'
]

RSVP_STATUSES = [
    'Awaiting Response',
    'Rsvp Coming',
    'Rsvp Not Coming',
    'No Rsvp'
]

# The list of all approval statuses for which a person could come
# e.g. "No Rsvp" means that person cannot come, but "Awaiting Response" could be a person
# This is used for bus route counting when we have a hard cap for how many people could be on the bus
# so a potential person has to count as a person
STATUSES_FOR_PEOPLE_TO_COUNT = [
    'Approved',
    'Awaiting Response',
    'Rsvp Coming'
]

STATS_STATUSES = [
    'approved',
    'emailed',
    'rsvpd'
]

CATEGORIES = [
    TRAVEL_RIDE_BUS,
    TRAVEL_PROVIDE_OWN_TRANSIT,
    TRAVEL_ALREADY_AT_UIUC,
    TRAVEL_NO_RESPONSE
]

BUS_ROUTES = [
    'Purdue',
    'Iowa St -> Grinnel -> Iowa',
    'Depaul -> Northwestern -> UIC',
    'IIT -> UChicago',
    'Michigan Tech -> Wisconsin',
    'Indiana -> Rose Hulman',
    'Missouri -> WashU',
    'Case Western -> Kent -> OSU',
    'Indiana -> Rose Hulman',
    'University of Michigan Ann-Arbor'
]

RESUME_MAX_SIZE = 2097152 # in Bytes = 2 mb

SCHOOLS = [
    'Binghamton University',
    'Bowling Green State University',
    'Bradley University',
    'Brown University',
    'Butler University',
    'California Institute of Technology',
    'Carnegie Mellon University',
    'Case Western Reserve University',
    'Colorado State University',
    'Columbia University',
    'Cornell University',
    'Depaul University',
    'Depauw University',
    'Drake University',
    'Drexel University',
    'Duke University',
    'Emory University',
    'Florida State University',
    'George Mason University',
    'Georgia Institute of Technology',
    'Grinnell College',
    'Harvard University',
    'Illinois Institute of Technology',
    'Illinois State University',
    'Indiana Institute of Technology',
    'Indiana University - Purdue University Indianapolis',
    'Indiana University Bloomington',
    'Indiana University',
    'Iowa State University',
    'Loyola University Chicago',
    'Macalester College',
    'Marquette University',
    'Massachusetts Institute of Technology (MIT)',
    'Michigan Institute of Technology',
    'Michigan State University',
    'Milwaukee School of Engineering',
    'Missouri University of Science and Technology',
    'New York University',
    'Northeastern Illinois University',
    'Northern Illinois University',
    'Northwestern University',
    'Notre Dame University',
    'Oakton Community College',
    'Oberlin College',
    'Ohio State University',
    'Ohio University',
    'Pennsylvania State University',
    'Princeton University',
    'Purdue University',
    'Rensselaer Polytechnic Institute',
    'Rhode Island School of Design',
    'Rice University',
    'Rose Hulman Institute of Technology',
    'Rutgers University',
    'Southern Connecticut State University',
    'Southern Illinois University - Carbondale',
    'Southern Illinois University - Edwardsville',
    'St. Louis University',
    'Stanford University',
    'Texas A&M University',
    'University of Buffalo',
    'University of California - Berkeley',
    'University of Central Florida',
    'University of Chicago',
    'University of Cincinnati',
    'University of Colorado - Boulder',
    'University of Dayton',
    'University of Georgia',
    'University of Illinois - Chicago',
    'University of Illinois - Springfield',
    'University of Illinois - Urbana-Champaign (UIUC)',
    'University of Iowa',
    'University of Maryland',
    'University of Michigan',
    'University of Minnesota',
    'University of Missouri',
    'University of Nebraska - Lincoln',
    'University of Pennsylvania',
    'University of Pittsburgh',
    'University of Texas-Austin',
    'University of Toledo',
    'University of Toronto',
    'University of Wisconsin - Madison',
    'University of Wisconsin - Milwaukee',
    'Vanderbilt University',
    'Virginia Institute of Technology',
    'Virginia Polytechnic Institute and State University (Virginia Tech)',
    'Washington University in St. Louis',
    'Worcester Polytechnic Institute',
    'Wright State University',
    'Yale University'
]


# List containing all the site URL's to test in unittests
TEST_SITE_URLS = [
    '/',
    # '/emailbackup',

    '/apply',
    '/apply/complete',
    '/apply/updated',
    '/apply/schoolcheck',
    '/apply/schoollist',
    # '/apply/myresume',
    '/apply/uploadurl',

    '/rules',
    '/schedule',
    '/travel',
    '/sponsor/faq',
    # '/tropo',
    '/code-of-conduct',

    '/sponsor/download',

    '/applycount',

    '/admin',
    '/admin/xkcd',
    '/admin/approve',
    '/admin/stats',
    '/admin/basicstats',
    '/admin/resume',
    '/admin/applycount',
    '/admin/schoolcount',
    '/admin/manager',
    '/admin/export',

    # '/admin/approve/<school>',
    # '/admin/profile/<userId>',

    # '/logout',

    '/mgt',
    '/particles',
]



