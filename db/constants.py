BUCKET = 'hackillinois'

APPLY_TITLE = 'Application'
PROFILE_TITLE = 'Profile'

ERROR_MESSAGE_PREFIX = 'Please enter '
ERROR_MESSAGE_SUFFIX = '.'

ALL_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'resume', 'linkedin', 'github', 'shirt', 'food', 'foodInfo', 'projectType', 'experience', 'termsOfService']
REQUIRED_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'year', 'shirt', 'experience', 'termsOfService']

# This should have *ALL* fields in REQUIRED_FIELDS *EXCEPT* for 'termsOfService'
READABLE_REQUIRED_FIELDS = {'nameFirst':'your First Name',
                            'nameLast':'your Last Name',
                            'email':'your valid E-mail Address',
                            'gender':'your Gender',
                            'school':'your School',
                            'year':'your Year in School',
                            'shirt':'your T-shirt size',
                            'experience':'your past experience'}
                            
TOS_ERROR_MESSAGE = 'Please accept the Terms of Service'

EMAIL_MATCH = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$"

GENDERS = ['Male','Female','Other', 'I choose not to specify']
YEARS = ['Freshman','Sophomore','Junior','Senior','Grad','HS']
SHIRTS = ['XS','S','M','L','XL','XXL']
FOODS = ['Vegetarian','Vegan','Gluten Free','Lactose Free', 'Other']
PROJECTS = ['Software Hack','Hardware Hack','Unsure']

RESUME_MAX_SIZE = 2097152 # in Bytes = 2 mb


SCHOOLS = {
    'binghamton.edu':'Binghamton University',
    'bgsu.edu':'Bowling Green State University',
    'bradley.edu':'Bradley University',
    'brown.edu':'Brown University',
    'buffalo.edu':'University of Buffalo',
    'butler.edu':'Butler University',
    'caltech.edu':'California Institute of Technology',
    'cmu.edu':'Carnegie Mellon University',
    'case.edu':'Case Western Reserve University',
    'colostate.edu':'Colorado State University',
    'columbia.edu':'Columbia University',
    'cornell.edu':'Cornell University',
    'depaul.edu':'Depaul University',
    'depauw.edu':'Depauw University',
    'drake.edu':'Drake University',
    'drexel.edu':'Drexel University',
    'duke.edu':'Duke University',
    'emory.edu':'Emory University',
    'fsu.edu':"Florida State University",
    'gatech.edu':'Georgia Institute of Technology',
    'gmu.edu':'George Mason University',
    'grinnell.edu':'Grinnell College',
    'harvard.edu':'Harvard University',
    'iit.edu':'Illinois Institute of Technology',
    'ilstu.edu':"Illinois State University",
    'indiana.edu':"Indiana University",
    'indianatech.edu':'Indiana Institute of Technology',
    'iub.edu':'Indiana University Bloomington',
    'iastate.edu':'Iowa State University',
    'iupui.edu':'Indiana University - Purdue University Indianapolis',
    'luc.edu':'Loyola University Chicago',
    'marquette.edu':'Marquette University',
    'macalester.edu':'Macalester College',
    'umd.edu':'University of Maryland',
    'mit.edu':'Massachusetts Institute of Technology',
    'mtu.edu':'Michigan Institute of Technology',
    'msu.edu':'Michigan State University',
    'msoe.edu':'Milwaukee School of Engineering',
    'mst.edu':'Missouri University of Science and Technology',
    'unl.edu':'University of Nebraska - Lincoln',
    'neiu.edu':'Northeastern Illinois University',
    'niu.edu':'Northern Illinois University',
    'northwestern.edu':'Northwestern University',
    'nd.edu':'Notre Dame University',
    'nyu.edu':'New York University',
    'oakton.edu':'Oakton Community College',
    'oberlin.edu':'Oberlin College',
    'osu.edu':'Ohio State University',
    'ohio.edu':'Ohio University',
    'psu.edu':'Pennsylvania State University',
    'princeton.edu':'Princeton University',
    'purdue.edu':'Purdue University',
    'rice.edu':"Rice University",
    'risd.edu':'Rhode Island School of Design',
    'rose-hulman.edu':'Rose Hulman Institute of Technology',
    'rpi.edu':"Rensselaer Polytechnic Institute",
    'rutgers.edu':'Rutgers University',
    'siu.edu':'Southern Illinois University - Carbondale',
    'siue.edu':'Southern Illinois University - Edwardsville',
    'slu.edu':'St. Louis University',
    'southernct.edu':'Southern Connecticut State University',
    'stanford.edu':'Stanford University',
    'berkeley.edu':'University of California - Berkeley',
    'uchicago.edu':'University of Chicago',
    'uc.edu':'University of Cincinnati',
    'colorado.edu':'University of Colorado - Boulder',
    'udayton.edu':'University of Dayton',
    'illinois.edu':'University of Illinois - Urbana-Champaign',
    'uiuc.edu':'University of Illinois - Urbana-Champaign',
    'uic.edu':'University of Illinois - Chicago',
    'uis.edu':'University of Illinois - Springfield',
    'uiowa.edu':'University of Iowa',
    'umd.edu':'University of Maryland',
    'umich.edu':'University of Michigan',
    'umn.edu':'University of Minnesota',
    'uga.edu':'University of Georgia',
    'missouri.edu':'University of Missouri',
    'upenn.edu':'University of Pennsylvania',
    'pitt.edu':'University of Pittsburgh',
    'tamu.edu':'Texas A&M University',
    'ucf.edu':'University of Central Florida',
    'utexas.edu':'University of Texas-Austin',
    'utoledo.edu':'University of Toledo',
    'utoronto.ca':"University of Toronto",
    'uwm.edu':'University of Wisconsin - Milwaukee',
    'wisc.edu':'University of Wisconsin - Madison',
    'wpi.edu':'Worcester Polytechnic Institute',
    'vanderbilt.edu':'Vanderbilt University',
    'vt.edu':'Virginia Institute of Technology',
    'wustl.edu':'Washington University in St. Louis',
    'wright.edu':'Wright State University',
    'yale.edu':'Yale University'
}
