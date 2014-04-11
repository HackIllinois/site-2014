ADMIN_EMAILS = set(['lx.icomputer@gmail.com','mvd7793@gmail.com','austin.1111h@gmail.com','fishben2@illinois.edu','jacob@hackillinois.org, brendanryan@hackillinois.org'])

BUCKET = 'hackillinois'

MEMCACHE_TIMEOUT = 10800 # seconds = 3 hours , once we close registration increase to 1 day
MOBILE_MEMCACHE_TIMEOUT = 86400 # second = 1 day (24 hours)
MEMCACHE_COUNT_TIMEOUT = 900 # seconds = 15 min
USE_ADMIN_MEMCACHE = False
USE_SPONSOR_MEMCACHE = False

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
RSVP_CLOSED_MESSAGE = 'We\'re sorry, but your RSVP deadline for HackIllinois has passed.<br>We may have released your spot to another hacker on the waitlist. <br><a href="mailto:contact@hackillinois.org" style="color: #ef3e36">Email us</a> to see if there\'s still space available. Happy hacking!'

ERROR_MESSAGE_PREFIX = 'Please provide '
ERROR_MESSAGE_SUFFIX = '.'

ATTENDEE_START_COUNT = 1
SPONSOR_START_COUNT = 10001
ADMIN_START_COUNT = 20001

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

SPONSOR_LOGOS = [
    { "href":"http://www.inin.com/",
      "alt":"Interactive Intelligence",
      "class":"sponsor-supernova",
      "src":"/img/logos/resized/inin.png",
      "br_after":False },
    { "href":"http://www.e-imo.com/",
      "alt":"imo",
      "class":"sponsor big",
      "src":"/img/logos/resized/imo.png",
      "br_after":False },
    { "href":"http://www.getpebble.com/",
      "alt":"pebble",
      "class":"sponsor big",
      "src":"/img/logos/resized/pebble.png",
      "br_after":True },
    { "href":"http://www.bloomberg.com",
      "alt":"bloomberg",
      "class":"sponsor big",
      "src":"/img/logos/resized/bloomberg.png",
      "br_after":False },
    { "href":"http://www.groupon.com",
      "alt":"groupon",
      "class":"sponsor big",
      "src":"/img/logos/resized/groupon.png",
      "br_after":False },
    { "href":"http://www.neustar.biz",
      "alt":"neustar",
      "class":"sponsor big",
      "src":"/img/logos/resized/neustar.png",
      "br_after":False },
    { "href":"http://www.statefarm.com",
      "alt":"state farm",
      "class":"sponsor big",
      "src":"/img/logos/resized/statefarm.png",
      "br_after":False },
    { "href":"http://www.venmo.com/",
      "alt":"venmo",
      "class":"sponsor big venmo",
      "src":"/img/logos/resized/venmo.png",
      "br_after":False },
    { "href":"http://www.westmonroepartners.com/",
      "alt":"west monroe partners",
      "class":"sponsor big s-padding-fix",
      "src":"/img/logos/resized/westmonroe.png",
      "br_after":False },
    { "href":"http://www.tcs.com/",
      "alt":"tcs",
      "class":"sponsor big",
      "src":"/img/logos/resized/tcs.png",
      "br_after":False },
    { "href":"http://www.niksun.com/",
      "alt":"niksun",
      "class":"sponsor big niksun",
      "src":"/img/logos/resized/niksun.png",
      "br_after":False },
    { "href":"http://www.answers.com/",
      "alt":"answers",
      "class":"sponsor big answers",
      "src":"/img/logos/resized/answers.png",
      "br_after":False },
    { "href":"http://www.goldmansachs.com",
      "alt":"goldman sachs",
      "class":"sponsor big goldmansachs",
      "src":"/img/logos/resized/goldman.png",
      "br_after":False },
    { "href":"http://www.wolfram.com",
      "alt":"wolfram",
      "class":"sponsor big",
      "src":"/img/logos/resized/wolfram.png",
      "br_after":False },
    { "href":"http://developer.deere.com",
      "alt":"john deere",
      "class":"sponsor big johndeere",
      "src":"/img/logos/resized/deere.png",
      "br_after":False },
    { "href":"http://www.trunkclub.com",
      "alt":"trunk club",
      "class":"sponsor big trunkclub",
      "src":"/img/logos/resized/trunk_club.png",
      "br_after":False },
    { "href":"http://www.yahoo.com",
      "alt":"yahoo",
      "class":"sponsor big",
      "src":"/img/logos/resized/yahoo.png",
      "br_after":False },
    { "href":"http://www.kcg.com",
      "alt":"kcg",
      "class":"sponsor big",
      "src":"/img/logos/kcg.png",
      "br_after":False },
    { "href":"http://www.ge.com",
      "alt":"general electric",
      "class":"sponsor big ge",
      "src":"/img/logos/g_e.png",
      "br_after":False },
    { "href":"http://www.allstontrading.com",
      "alt":"allston trading",
      "class":"sponsor big allston",
      "src":"/img/logos/allston.png",
      "br_after":False },
    { "href":"http://www.dropbox.com",
      "alt":"dropbox",
      "class":"sponsor little s-padding-fix",
      "src":"/img/logos/resized/dropbox.png",
      "br_after":False },
    { "href":"http://www.google.com",
      "alt":"google",
      "class":"sponsor little s-padding-fix",
      "src":"/img/logos/resized/google.png",
      "br_after":False },
    { "href":"http://www.citadel.com",
      "alt":"citadel",
      "class":"sponsor little",
      "src":"/img/logos/resized/citadel.png",
      "br_after":False },
    { "href":"http://www.mailgun.com",
      "alt":"mailgun",
      "class":"sponsor little mailgun",
      "src":"/img/logos/resized/mailgun.png",
      "br_after":False },
    { "href":"http://www.spottradingllc.com",
      "alt":"spot trading",
      "class":"sponsor little spot-trading",
      "src":"/img/logos/resized/spottrading.png",
      "br_after":False },
    { "href":"http://www.epic.com",
      "alt":"epic systems",
      "class":"sponsor little epic",
      "src":"/img/logos/resized/epic.png",
      "br_after":False },
    { "href":"http://www.bankofamerica.com",
      "alt":"bank of america",
      "class":"sponsor little",
      "src":"/img/logos/bofa.png",
      "br_after":False },
    { "href":"http://www.spiceworks.com",
      "alt":"spiceworks",
      "class":"sponsor little",
      "src":"/img/logos/spiceworks.png",
      "br_after":False },
    { "href":"http://www.electricimp.com",
      "alt":"electric imp",
      "class":"sponsor littler",
      "src":"/img/logos/resized/electricimp.png",
      "br_after":False },
    { "href":"http://www.octopart.com",
      "alt":"octopart",
      "class":"sponsor littler",
      "src":"/img/logos/resized/octopart.png",
      "br_after":False },
    { "href":"http://www.sparkfun.com",
      "alt":"sparkfun",
      "class":"sponsor littler",
      "src":"/img/logos/resized/sparkfun.png",
      "br_after":False },
    { "href":"http://www.rdio.com",
      "alt":"rdio",
      "class":"sponsor littler rdio",
      "src":"/img/logos/resized/rdio.png",
      "br_after":False },
    { "href":"http://www.lob.com",
      "alt":"lob",
      "class":"sponsor littler lob",
      "src":"/img/logos/resized/lob.png",
      "br_after":False },
    { "href":"http://www.firebase.com",
      "alt":"firebase",
      "class":"sponsor littler firebase",
      "src":"/img/logos/resized/firebase.png",
      "br_after":False },
    { "href":"http://www.makerlab.illinois.edu",
      "alt":"makerlab",
      "class":"sponsor littler",
      "src":"/img/logos/resized/makerlab.png",
      "br_after":False },
    { "href":"http://www.etsy.com",
      "alt":"etsy",
      "class":"sponsor littler etsy",
      "src":"/img/logos/etsy.png",
      "br_after":False },
    { "href":"http://www.microsoft.com",
      "alt":"microsoft",
      "class":"sponsor littler microsoft",
      "src":"/img/logos/resized/microsoft.png",
      "br_after":False },
    { "href":"http://www.facebook.com",
      "alt":"facebook",
      "class":"sponsor littler",
      "src":"/img/logos/resized/facebook.png",
      "br_after":False },
    { "href":"http://www.intel.com",
      "alt":"intel",
      "class":"sponsor littler intel",
      "src":"/img/logos/resized/intel.png",
      "br_after":False },
    { "href":"http://www.namecheap.com",
      "alt":"namecheap",
      "class":"sponsor littler",
      "src":"/img/logos/resized/namecheap.png",
      "br_after":False },
    { "href":"http://www.a16z.com",
      "alt":"Andreessen Horowitz",
      "class":"sponsor littler",
      "src":"/img/logos/resized/a16z.png",
      "br_after":False },
    { "href":"http://www.dwolla.com",
      "alt":"dwolla",
      "class":"sponsor littler",
      "src":"/img/logos/resized/dwolla.png",
      "br_after":False },
    { "href":"http://www.twilio.com",
      "alt":"twilio",
      "class":"sponsor littler",
      "src":"/img/logos/resized/twilio.png",
      "br_after":False },
    { "href":"http://www.hudl.com",
      "alt":"hudl",
      "class":"sponsor littler",
      "src":"/img/logos/hudl.png",
      "br_after":False },
    { "href":"http://www.akunacapital.com",
      "alt":"akuna capital",
      "class":"sponsor littler",
      "src":"/img/logos/akuna.png",
      "br_after":False },
    { "href":"http://www.newark.com",
      "alt":"newark",
      "class":"sponsor littler",
      "src":"/img/logos/newark.png",
      "br_after":False },
    { "href":"http://www.3red.com",
      "alt":"3Red",
      "class":"sponsor littler three_red",
      "src":"/img/logos/3Red.png",
      "br_after":False },
    { "href":"http://www.stickermule.com",
      "alt":"stickermule",
      "class":"sponsor littler",
      "src":"/img/logos/resized/stickermule.png",
      "br_after":False },
    { "href":"http://orbitz.com",
      "alt":"orbitz",
      "class":"sponsor littler",
      "src":"/img/logos/resized/orbitz.png",
      "br_after":False },
    { "href":"http://spark.io",
      "alt":"spark.io",
      "class":"sponsor littler sparkio",
      "src":"/img/logos/resized/sparkio.png",
      "br_after":False },
    { "href":"http://parrot.com",
      "alt":"parrot",
      "class":"sponsor littler",
      "src":"/img/logos/resized/parrot.png",
      "br_after":False },
    { "href":"http://pwc.com",
      "alt":"pwc",
      "class":"sponsor littler pwc",
      "src":"/img/logos/resized/pwc.png",
      "br_after":False },
    { "href":"http://zealousamoeba.com",
      "alt":"zealous amoeba",
      "class":"sponsor littler z_a",
      "src":"/img/logos/za.png",
      "br_after":False },
    { "href":"http://onenorth.com",
      "alt":"one north",
      "class":"sponsor littler z_a",
      "src":"/img/logos/onenorth.png",
      "br_after":False },
]
