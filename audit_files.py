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

tree = ET.parse(INPUT_FILE)
root = tree.getroot()

bad_ids = []
bad_uids = []
bad_street_names = {} # Using a dictionary to store counts
bad_loc_values = [] # Stores bad lon and lat values
bad_postcodes = {} # Dictionary to store counts again

expected_street_names = ["Street", "Avenue", "Court", "Drive", "Boulevard", "Way", "Terrace", "Alley", "Place", "Lane", "Plaza", "Hill", "Circle", "Road", "Row"]

def audit_id(string): 
    try:
        int(string)
    except:
        bad_ids.append(string)

def audit_lon_lat(string):
    try:
        float(string)
    except:
        bad_loc_values.append(string)

def audit_street_name(string):
    words = string.split()
    for word in words:
        if len(word) == 1:
            print "Bad street name: " + string
    if words[-1] not in expected_street_names:
        print "Inconsistent street name: " + string
    pass

def audit_postcode(string):
    if string.startswith("941"):
        return string
    else:
        print "Bad post code: " + string

def audit_file(filename):
    # This function audits the input file
    for event, elem in ET.iterparse(filename, events = ("start",)):
        if elem.tag == "node" or elem.tag == "way":
            print event
            print elem

audit_file(INPUT_FILE)
