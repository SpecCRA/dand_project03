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
bad_street_names = {} # Using a dictionary to store counts
bad_loc_values = [] # Stores bad lon and lat values
bad_postcodes = {} # Dictionary to store counts again

expected_street_names = ["Street", "Avenue", "Court", "Drive", "Boulevard", "Way", "Terrace", "Alley", "Place", "Lane", "Plaza", "Hill", "Circle", "Road", "Row"]

def audit_id(string):
    """
    Takes a string and tries to make it an integer.
    ID values, both ID and UID should be able to be integers.
    
    Bad ID values get appended to a list.
    """
    try:
        int(string)
        return string
    except:
        bad_ids.append(string)

def audit_lon_lat(string):
    """
    Takes a string and tries make the string into a float type.
    Lat and lon values should both be float values in our dataset.
    
    Bad values get appended to a list.
    """
    try:
        float(string)
        return string
    except:
        bad_loc_values.append(string)

def audit_street_name(string):
    """
    Takes a string and checks the street name with the standard from the expected
    street names list. It also checks if any word in the street name is one letter
    to check for abbreviations in directions.

    Bad street names get appended to a dictioanry with a count.
    """
    words = string.split()
    for word in words:
        if len(word) == 1: # checks for one letter words
            print "Bad street name: " + string
    if words[-1] not in expected_street_names:
        try:
            bad_street_names[string] += 1
        except:
            bad_street_names[string] = 1
        #print "Inconsistent street name: " + string

def audit_postcode(string):
    """
    Takes a string and checks if the postal code is valid and consistent with
    the city and county of San Francisco.

    Bad values get added to a dictionary with a count.
    """
    if string.startswith("941"):
        return string
    else:
        try:
            bad_postcodes[string] += 1
        except:
            bad_postcodes[string] = 1

def audit_file(filename):
    # This function audits the input file
    for event, elem in ET.iterparse(filename, events = ("start",)):
        if elem.tag == "node" or elem.tag == "way":
            continue
            print event
            print elem

def print_values(ids, loc_values, street_names, postcodes):

    for n in ids:
        print "Bad id value: " + str(n)

    for n in loc_values:
        print "Bad location value: " + str(n)
    print "Bad street names: \n"
    pprint.pprint(street_names, width=1)
    print "Bad postcodes: \n"
    pprint.pprint(postcodes, width=1)

#audit_file(INPUT_FILE)
#print_values(bad_ids, bad_loc_values, bad_street_names, bad_postcodes)
