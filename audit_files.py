#!/usr/bin/env python


import pprint
import re
import xml.etree.cElementTree as ET

"""
This is the auditing file.
Preliminary checks:
1. All values are they they should be as in id's are integers, lon 
and lat values are floats
2. Consistencies in street name nomenclature 
3. Consistency in county and city values
4. Consistency in postal code
5. Correct postal code (Starts with 941 for San Francisco)
"""

