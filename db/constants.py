ADMIN_EMAILS = set(['lx.icomputer@gmail.com','mvd7793@gmail.com','austin.1111h@gmail.com','fishben2@illinois.edu'])

BUCKET = 'hackillinois'

MEMCACHE_TIMEOUT = 10800 # seconds = 3 hours , once we close registration increase to 1 day
MEMCACHE_COUNT_TIMEOUT = 900 # seconds = 15 min

APPLY_TITLE = 'Application'
PROFILE_TITLE = 'Profile'

APPLY_COMPLETE_HEADER = 'Application Complete!'
APPLY_COMPLETE_MESSAGE = 'Thanks for applying! To keep in touch, follow us on Facebook and Twitter. Also, don\'t forget to RSVP to the <a href="https://www.facebook.com/events/285744431573053" target="_blank" style="color: #ef3e36">Facebook event</a>!'

UPDATE_COMPLETE_HEADER = 'Application Updated!'
UPDATE_COMPLETE_MESSAGE = 'Thanks for updating your application!<br>To keep in touch, follow us on Facebook and Twitter.<br>Also, don\'t forget to RSVP to the <a href="https://www.facebook.com/events/285744431573053" target="_blank" style="color: #ef3e36">Facebook event</a>!'

ERROR_MESSAGE_PREFIX = 'Please provide '
ERROR_MESSAGE_SUFFIX = '.'

ALL_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'resume', 'linkedin', 'github', 'shirt', 'food', 'foodInfo', 'projectType', 'experience', 'termsOfService']
REQUIRED_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'shirt', 'experience']

# This should have *ALL* fields in REQUIRED_FIELDS *EXCEPT* for 'termsOfService'
READABLE_REQUIRED_FIELDS = {'nameFirst':'your first name',
                            'nameLast':'your last name',
                            'email':'your valid e-mail address',
                            'gender':'your gender',
                            'school':'your school',
                            'year':'your year in school',
                            'shirt':'your T-shirt size',
                            'experience':'your past experience',
                            'projectType':'your project type'}

READABLE_FIELDS = {'food':'your dietary restrictions',
                   'food-info':'your dietary restriction information'}

TOS_ERROR_MESSAGE = 'Please accept the Terms of Service'

CSV_HEADINGS = ['First Name','Last Name','Email',
                'Gender','School','Year','LinkedIn',
                'Github','Shirt','Food','Project Type',
                'Registration Time','Is Approved',
                'User ID','Resume']

# The below array is for more descriptive error messages. @Mattato pls fix.
# READABLE_REQUIRED_FIELDS = ['First Name','Last Name','E-mail','Gender','School','Year in School','T-shirt size','past experience', 'Please accept the Terms of Service']

EMAIL_MATCH = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$"

GENDERS = ['Male','Female','Other', 'I choose not to specify']
YEARS = ['Freshman','Sophomore','Junior','Senior','Grad','HS']
SHIRTS = ['XS','S','M','L','XL','XXL']
FOODS = ['Vegetarian','Vegan','Gluten Free','Lactose Free', 'Other']
PROJECTS = ['Software Hack','Hardware Hack','Unsure']

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

    # '/logout',

    '/mgt',
    '/particles',
]



