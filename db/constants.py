ADMIN_EMAILS = set(['lx.icomputer@gmail.com','mvd7793@gmail.com','austin.1111h@gmail.com','fishben2@illinois.edu','jacob@hackillinois.org, brendanryan@hackillinois.org'])

BUCKET = 'hackillinois'

TWILIO_ACCOUNT_SID = "ACbb49f22ced63701bdc7e7391489d1720"
TWILIO_AUTH_TOKEN = "77878e6db49a1635bf767dc64d203a5b"

ALWAYS_ENABLED_URLS = [ "a98c0" ]

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
PHONE_MATCH = r"\+1\d{10}"

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
    { "href":"http://developers.kloudless.com/",
      "alt":"kloudless",
      "class":"sponsor littler",
      "src":"/img/logos/kloudless.png",
      "br_after":False },
]

RESEARCH_PEPPER = "yDbC43w7Xj22LK3Xxh6Z3fy628x8md6w"

ATTENDEE_NUMBERS = [
    "+14196104393",
    "+19083613629",
    "+12017835047",
    "+15135493890",
    "+19204700567",
    "+16147495702",
    "+17342237932",
    "+16305576017",
    "+13013185042",
    "+18122011922",
    "+19894827371",
    "+12173775261",
    "+16109087871",
    "+12178192824",
    "+13198550779",
    "+19206981376",
    "+15743606139",
    "+18479429219",
    "+18604360774",
    "+16309564033",
    "+16306490483",
    "+12179798738",
    "+17632916339",
    "+18177037925",
    "+16304641140",
    "+14802748003",
    "+15025920003",
    "+14088909195",
    "+12177213408",
    "+16145565960",
    "+18158612519",
    "+15135932798",
    "+12672106878",
    "+17132020661",
    "+19143292696",
    "+17203179831",
    "+18475024279",
    "+16306674015",
    "+12199166858",
    "+14123783637",
    "+12246160771",
    "+16087707596",
    "+17029853909",
    "+16308999082",
    "+18122299118",
    "+17657202331",
    "+14085696058",
    "+19012373207",
    "+15135092086",
    "+12178997850",
    "+13093107482",
    "+14255187342",
    "+16307309066",
    "+12243928725",
    "+12178982996",
    "+19894139708",
    "+13146060587",
    "+17089555763",
    "+13105271827",
    "+16177840260",
    "+14126953420",
    "+12174192012",
    "+16303107664",
    "+15199967698",
    "+12083405914",
    "+19376210821",
    "+16189796953",
    "+16309270027",
    "+16189254073",
    "+13478785380",
    "+16149158886",
    "+12174185707",
    "+16197421221",
    "+19526076611",
    "+18324251431",
    "+16518087471",
    "+18122519202",
    "+17028584732",
    "+16304561292",
    "+15733010411",
    "+19375640234",
    "+14084204554",
    "+17325015976",
    "+15135036022",
    "+13124516168",
    "+18575378583",
    "+18476090468",
    "+18479773447",
    "+18162105075",
    "+16092502295",
    "+14192652354",
    "+12242348432",
    "+12245671146",
    "+19732169810",
    "+12179740320",
    "+18479778480",
    "+12248291887",
    "+16178512276",
    "+16085146261",
    "+14084775548",
    "+15133634435",
    "+17654090425",
    "+16306674593",
    "+16088868763",
    "+12178190257",
    "+16309158095",
    "+19546491770",
    "+13096439349",
    "+15713146381",
    "+13147759588",
    "+17736338573",
    "+14179880783",
    "+16309355665",
    "+19782898426",
    "+17035054087",
    "+12144786151",
    "+17738369102",
    "+12179740418",
    "+12016746599",
    "+18134101021",
    "+15038402228",
    "+19198892549",
    "+16094239159",
    "+17329865371",
    "+15024179758",
    "+13122130525",
    "+16302072339",
    "+16108833912",
    "+17088285713",
    "+12533326171",
    "+16305406002",
    "+16159748233",
    "+13194006596",
    "+12489241816",
    "+19174205338",
    "+18153546377",
    "+16308906224",
    "+12179745278",
    "+16309577057",
    "+17654182062",
    "+19062315300",
    "+12482523663",
    "+16363591630",
    "+12174135413",
    "+12179798232",
    "+19797398574",
    "+13475585608",
    "+18473810832",
    "+17735522539",
    "+18154742509",
    "+12012749689",
    "+12625730133",
    "+16157889749",
    "+16302094756",
    "+18123813984",
    "+19258998130",
    "+13146805482",
    "+17148094839",
    "+16308423829",
    "+13126616491",
    "+18477705531",
    "+15735297234",
    "+12242510436",
    "+12243266039",
    "+17326874015",
    "+16307029258",
    "+15743830385",
    "+17737546817",
    "+17738277496",
    "+13097127216",
    "+13316423140",
    "+16305967930",
    "+16189721757",
    "+12176074446",
    "+18476369428",
    "+16306972626",
    "+17733123301",
    "+16305502512",
    "+12173413353",
    "+18475711305",
    "+17344783974",
    "+14146141337",
    "+12039092404",
    "+12178983636",
    "+17657210874",
    "+13308583907",
    "+13123078870",
    "+12246281364",
    "+17739726147",
    "+16306158897",
    "+17654364923",
    "+12024684461",
    "+16165589991",
    "+17088708822",
    "+16508674951",
    "+17324252913",
    "+18475335499",
    "+16307307981",
    "+13194312634",
    "+18472198009",
    "+13146834546",
    "+13098245732",
    "+16302769472",
    "+13128416503",
    "+16304649902",
    "+12179790379",
    "+16308641918",
    "+18476309958",
    "+12014526352",
    "+13146061887",
    "+15129223599",
    "+15739829244",
    "+18656220501",
    "+15133311119",
    "+13035074232",
    "+19375438367",
    "+18156418762",
    "+12177966933",
    "+16517577031",
    "+16302071793",
    "+12487705692",
    "+18154810881",
    "+15135930845",
    "+14126385326",
    "+13146777847",
    "+16306324536",
    "+18627549149",
    "+19894883855",
    "+12176499936",
    "+16309910910",
    "+13124796011",
    "+12625040387",
    "+17734908497",
    "+12179793603",
    "+16083015316",
    "+14254443966",
    "+16363284049",
    "+15104612786",
    "+17083369630",
    "+12179745127",
    "+18167286516",
    "+12174199896",
    "+12178196126",
    "+18163040031",
    "+15712693026",
    "+19205745623",
    "+18479207383",
    "+15132807366",
    "+15177067731",
    "+14252098743",
    "+14193779502",
    "+12674211439",
    "+17082077456",
    "+16304008831",
    "+16302800447",
    "+14259999197",
    "+18477160876",
    "+19082408122",
    "+17349297515",
    "+16302721691",
    "+17817890338",
    "+16572069657",
    "+12178980753",
    "+16304845159",
    "+12245580568",
    "+12244066550",
    "+15137038091",
    "+12144050139",
    "+12178986722",
    "+18478497817",
    "+19178159522",
    "+12174186703",
    "+19498360413",
    "+12172745855",
    "+18477701508",
    "+12177217838",
    "+19144069294",
    "+19378480987",
    "+16304576219",
    "+19788440961",
    "+16517056118",
    "+12175502691",
    "+17087670703",
    "+18122363195",
    "+16083542816",
    "+14152333348",
    "+15174025315",
    "+13109754225",
    "+12672301309",
    "+12174195750",
    "+18477146444",
    "+14432447814",
    "+12178190164",
    "+18057980216",
    "+13105610731",
    "+15042028250",
    "+16307880294",
    "+14083065368",
    "+18472042727",
    "+12032498911",
    "+12623098055",
    "+17739683221",
    "+19524522029",
    "+15203311257",
    "+13194009649",
    "+16309039066",
    "+18479873073",
    "+16142856786",
    "+18478487670",
    "+12173771571",
    "+18322397385",
    "+12484943549",
    "+13193338724",
    "+16968813486",
    "+13102614726",
    "+17164000899",
    "+12179740615",
    "+12489306329",
    "+12605713660",
    "+12176076901",
    "+16314876510",
    "+17739545739",
    "+16304184412",
    "+18026623642",
    "+14693963850",
    "+16303037034",
    "+12242100576",
    "+13144985006",
    "+17733320051",
    "+16308160742",
    "+17083168669",
    "+17173858845",
    "+13125324203",
    "+12035287210",
    "+13128523629",
    "+18474779931",
    "+15733370877",
    "+12178830368",
    "+16306188778",
    "+16305121368",
    "+12178986980",
    "+13015027819",
    "+19788860146",
    "+12606570115",
    "+17188871021",
    "+16303627310",
    "+17656373307",
    "+15745278811",
    "+12174199414",
    "+16306052511",
    "+12485203071",
    "+12178987302",
    "+12484162559",
    "+14172092813",
    "+14199021160",
    "+14083209933",
    "+17739792971",
    "+16308123540",
    "+17186126039",
    "+16304294087",
    "+17603156444",
    "+13097164562",
    "+12176667009",
    "+16308199544",
    "+13177500727",
    "+15174105282",
    "+15167328880",
    "+13107936293",
    "+16178716239",
    "+12177664300",
    "+17082033578",
    "+12314925380",
    "+15136005626",
    "+12177216203",
    "+17086794014",
    "+13114009947",
    "+16307309432",
    "+17656672132",
    "+18186618088",
    "+16302004025",
    "+14405396752",
    "+12172812507",
    "+16512306401",
    "+12168358194",
    "+15626506177",
    "+18479976485",
    "+18018006644",
    "+17325434072",
    "+17735438896",
    "+15135935288",
    "+12243218921",
    "+15166724839",
    "+17328871131",
    "+18475715310",
    "+16083957313",
    "+14085824781",
    "+16104162891",
    "+18122292532",
    "+14057622905",
    "+13147578266",
    "+19254871089",
    "+16308091660",
    "+18473129232",
    "+15027776385",
    "+17087104306",
    "+15072540402",
    "+12242120088",
    "+12178199259",
    "+16302009613",
    "+13146808584",
    "+15103167046",
    "+13127259699",
    "+12177216313",
    "+12178191055",
    "+12178987983",
    "+12176076680",
    "+17035820822",
    "+16125642352",
    "+13098388801",
    "+14407598400",
    "+16023614176",
    "+12178980326",
    "+12179797595",
    "+18479771662",
    "+18157939944",
    "+16304012886",
    "+12178985277",
    "+15202031108",
    "+12178197556",
    "+12176932123",
    "+13302858658",
    "+16303982857",
    "+12246262674",
    "+13039412863",
    "+14259224625",
    "+16092165664",
    "+13174167556",
    "+18168305123",
    "+16086205094",
    "+17049989576",
    "+17657756912",
    "+12179793665",
    "+16462297509",
    "+17737068978",
    "+12178985769",
    "+18478634966",
    "+19544153337",
    "+16302011110",
    "+12178988946",
    "+15037307807",
    "+16266441497",
    "+16308499267",
    "+16304058454",
    "+14142071898",
    "+17874498364",
    "+12247300487",
    "+12242006125",
    "+13016480039",
    "+13123610876",
    "+15072466181",
    "+16363888236",
    "+17082150321",
    "+12175502501",
    "+12174806350",
    "+14083873114",
    "+18474099014",
    "+13148537371",
    "+16262191649",
    "+17088339788",
    "+15074010670",
    "+16086286919",
    "+16302473096",
    "+17038811188",
    "+14085078068",
    "+18473222162",
    "+12174175825",
    "+12242007866",
    "+17653371642",
    "+13195300934",
    "+19292000906",
    "+12252888399",
    "+16262319022",
    "+16303625408",
    "+13097371661",
    "+18123744601",
    "+16025012481",
    "+17654091459",
    "+16308085531",
    "+15105796588",
    "+12018415548",
    "+18183967648",
    "+13127318264",
    "+16302072715",
    "+16306151818",
    "+12178187557",
    "+16304533327",
    "+17737150766",
    "+16304142588",
    "+12245672860",
    "+16185203196",
    "+12482104014",
    "+17655411540",
    "+16784711439",
    "+12178197803",
    "+18472099371",
    "+18473848019",
    "+12174198123",
    "+15199967684",
    "+16304858711",
    "+12178532100",
    "+14089168881",
    "+12176073089",
    "+14086606699",
    "+17406410248",
    "+18476023979",
    "+13097518987",
    "+18477145734",
    "+17195571229",
    "+13239429374",
    "+19086982576",
    "+18476209545",
    "+14175226445",
    "+16186104506",
    "+12178190299",
    "+18327824580",
    "+16785106337",
    "+15037085826",
    "+12488545692",
    "+17734902252",
    "+17083052273",
    "+17736036536",
    "+18475052846",
    "+18472207549",
    "+12172812816",
    "+18586529139",
    "+14083183895",
    "+15039229663",
    "+16518959975",
    "+13093977556",
    "+15129246597",
    "+18478901374",
    "+12248051366",
    "+13172607739",
    "+18186312102",
    "+12314092318",
    "+12625068406",
    "+15742296840",
    "+15743449628",
    "+14122533165",
    "+12175508850",
    "+12178192553",
    "+12177787996",
    "+12172812774",
    "+19373052230",
    "+16169011776",
    "+18476367905",
    "+13134056108",
    "+18158148770",
    "+16464681441",
    "+16362363288",
    "+13303473746",
    "+14157469623",
    "+12174199167",
    "+12176076541",
    "+16309170868",
    "+15732685421",
    "+17737189291",
    "+17736535969",
    "+13104981528",
    "+12176074131",
    "+14143360931",
    "+12629899862",
    "+16504549345",
    "+13179641221",
    "+13122135143",
    "+13173748832",
    "+13174903924",
    "+14252691528",
    "+16307152135",
    "+17083819295",
    "+16304568083",
    "+19252169095",
    "+13195940641",
    "+16165164598",
    "+16162985938",
    "+14157792390",
    "+12179745128",
    "+17085485561",
    "+18159227904",
    "+19492593395",
    "+12179793611",
    "+12177211428",
    "+18562654167",
    "+13179899432",
    "+16303739347",
    "+18125954667",
    "+18479998757",
    "+12175023539",
    "+15012000320",
    "+17329101151",
    "+18479421088",
    "+12174188368",
    "+12175562003",
    "+19083312630",
    "+16308817203",
    "+19787902291",
    "+16309013805",
    "+12244101088",
    "+12175502442",
    "+13126089740",
    "+14072277659",
    "+14027304097",
    "+12488545690",
    "+13125760512",
    "+13124049823",
    "+18476264589",
    "+12247724244",
    "+15129833000",
    "+18473401206",
    "+19259637175",
    "+17736123678",
    "+18473375901",
    "+16154972551",
    "+19168689743",
    "+15417409943",
    "+16155792956",
    "+12177225933",
    "+14088237789",
    "+13124279091",
    "+16098657022",
    "+12034149271",
    "+17089490113",
    "+12246223334",
    "+12566941240",
    "+12172553147",
    "+12178980513",
    "+16306058694",
    "+16304708069",
    "+16306054194",
    "+12173776470",
    "+12178988345",
    "+17739960891",
    "+12178197350",
    "+12178197799",
    "+12176931197",
    "+17085745259",
    "+16306312005",
    "+16309035050",
    "+16145629704",
    "+18473374803",
    "+18153882039",
    "+17473336701",
    "+13478380313",
    "+18474970451",
    "+18322880511",
    "+12176932819",
    "+13304093009",
    "+13476575287",
    "+12178197982",
    "+16304870039",
    "+12242169174",
    "+17082597183",
    "+17089218463",
    "+17325993856",
    "+19193490686",
    "+18156777925",
]
