BUCKET = 'hackillinois'

REQUIRED_FIELDS = ['nameFirst', 'nameLast', 'email', 'gender', 'school', 'standing',
                   'resume', 'shirt', 'food', 'picture', 'termsOfService']

EMAIL_MATCH = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$"

GENDERS = ['Male','Female','I choose not to specify']
STANDINGS = ['Freshman','Sophomore','Junior','Senior','Grad','HS','Other']
SHIRTS = ['XS','S','M','L','XL','XXL']
FOODS = ['None','Vegetarian','Vegan','Gluten Free','Other']
PROJECTS = ['Software Hack','Hardware Hack','Unsure']

RESUME_MAX_SIZE = 2097152 # in Bytes = 2 mb

SCHOOLS = {
    'binghamton.edu':'Binghamton University',
    'bgsu.edu':'Bowling Green State University',
    'bradley.edu':'Bradley University',
    'brown.edu':'Brown University',
    'butler.edu':'Butler University',
    'caltech.edu':'California Institute of Technology',
    'cmu.edu':'Carnegie Mellon University',
    'case.edu':'Case Western Reserve University',
    'colostate.edu':'Colorado State University',
    'cornell.edu':'Cornell University',
    'depaul.edu':'Depaul University',
    'depauw.edu':'Depauw University',
    'drake.edu':'Drake University',
    'duke.edu':'Duke University',
    'emory.edu':'Emory University',
    'gatech.edu':'Georgia Institute of Technology',
    'grinnell.edu':'Grinnell College',
    'harvard.edu':'Harvard University',
    'iit.edu':'Illinois Institute of Technology',
    'isu.edu':'Illinois State University',
    'indianatech.edu':'Indiana Institute of Technology',
    'iub.edu':'Indiana University Bloomington',
    'iastate.edu':'Iowa State University',
    'iupui.edu':'Indiana University - Purdue University Indianapolis',
    'luc.edu':'Loyola University Chicago',
    'marquette.edu':'Marquette University',
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
    'osu.edu':'Ohio State University',
    'ohio.edu':'Ohio University',
    'psu.edu':'Pennsylvania State University',
    'princeton.edu':'Princeton University',
    'purdue.edu':'Purdue University',
    'rose-hulman.edu':'Rose Hulman Institute of Technology',
    'rutgers.edu':'Rutgers University',
    'siu.edu':'Southern Illinois University - Carbondale',
    'siue.edu':'Southern Illinois University - Edwardsville',
    'slu.edu':'St. Louis University',
    'stanford.edu':'Stanford University',
    'berkeley.edu':'University of California - Berkeley',
    'uchicago.edu':'University of Chicago',
    'uc.edu':'University of Cincinnati',
    'colorado.edu':'University of Colorado - Boulder',
    'udayton.edu':'University of Dayton',
    'illinois.edu':'University of Illinois - Urbana-Champaign',
    'uic.edu':'University of Illinois - Chicago',
    'uis.edu':'University of Illinois - Springfield',
    'uiowa.edu':'University of Iowa',
    'umd.edu':'University of Maryland',
    'umich.edu':'University of Michigan',
    'umn.edu':'University of Minnesota',
    'missouri.edu':'University of Missouri',
    'upenn.edu':'University of Pennsylvania',
    'pitt.edu':'University of Pittsburgh',
    'utexas.edu':'University of Texas-Austin',
    'utoledo.edu':'University of Toledo',
    'uwm.edu':'University of Wisconsin - Milwaukee',
    'wisc.edu':'University of Wisconsin - Madison',
    'vanderbilt.edu':'Vanderbilt University',
    'vt.edu':'Virginia Institute of Technology',
    'wustl.edu':'Washington University in St. Louis',
    'wright.edu':'Wright State University',
    'yale.edu':'Yale University'
}