import sys
import os

# Include third party libraries
third_party = os.path.join(os.path.dirname(__file__), 'third_party')
sys.path.append(third_party)

# Include tropo so we can just import tropo
sys.path.append(os.path.join(third_party, 'tropo-webapi-python'))