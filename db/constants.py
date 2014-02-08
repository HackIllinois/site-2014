BUCKET = 'hackillinois'

APPLY_TITLE = 'Application'
PROFILE_TITLE = 'Profile'

APPLY_COMPLETE_HEADER = 'Application Complete!'
APPLY_COMPLETE_MESSAGE = 'Thanks for applying! To keep in touch, follow us on Facebook and Twitter. Also, don\'t forget to RSVP to the <a href="https://www.facebook.com/events/285744431573053" target="_blank" style="color: #ef3e36">Facebook event</a>!'

UPDATE_COMPLETE_HEADER = 'Application Updated!'
UPDATE_COMPLETE_MESSAGE = 'Thanks for updating your application!<br>To keep in touch, follow us on Facebook and Twitter.<br>Also, don\'t forget to RSVP to the <a href="https://www.facebook.com/events/285744431573053" target="_blank" style="color: #ef3e36">Facebook event</a>!'

ERROR_MESSAGE_PREFIX = 'Please provide a valid '
ERROR_MESSAGE_SUFFIX = '.'

ALL_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'resume', 'linkedin', 'github', 'shirt', 'food', 'foodInfo', 'projectType', 'experience', 'termsOfService']
REQUIRED_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'shirt', 'experience']

FIELD_DISPLAY_NAMES = {'First Name',
                       'Last Name',
                       'Email',
                       'Gender',
                       'School',
                       'Year in School',
                       'Resume',
                       'LinkedIn Profile',
                       'Github Username',
                       'Shirt Size',
                       'Dietary Restriction',
                       'Food Info',
                       'Project Type',
                       'Previous Experience',
                       'Terms Of Service'}

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