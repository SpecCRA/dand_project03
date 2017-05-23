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

INPUT_FILE = "sf_sunset_district.osm"

expected_street_names = ["Street", "Avenue", "Court", "Drive", "Boulevard", "Way", "Terrace", "Alley", "Place", "Lane", "Plaza", "Hill", "Circle", "Road", "Row"]

def check_int(string):
    try:
        int(string)
    except:
        continue
def check_float(string):
    try:
        float(string):
    except:
        continue

def audit_street_name(elem):
    if elem.atrrib['k'] == "addr:stret":
        pass

def audit_file(filename):
    # first check if IDs and UIDs are integers
    for event, elem in ET.iterparse(filename, events = ("start",)):
        if elem.tag == "node" or elem.tag == "way":
            print event
            print elem

audit_file(INPUT_FILE)
