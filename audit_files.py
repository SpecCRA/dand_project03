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

INPUT_FILE = "seattle_ballard.xml"

tree = ET.parse(INPUT_FILE)
root = tree.getroot()

bad_ids = []
bad_street_names = {} # Using a dictionary to store counts
bad_loc_values = [] # Stores bad lon and lat values
bad_postcodes = {} # Dictionary to store counts again

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

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
    """
    This function audits the XML input file to check IDs, UIDs, latitude, longitude, street
    names, and post codes.
    """
    for event, elem in ET.iterparse(filename, events = ("start",)):
        if elem.tag == "node" or elem.tag == "way":
            #print event
            #print elem
            for attrName, attrValue in elem.attrib.items():
                if attrName == "id":
                    audit_id(attrValue)
                elif attrName == "uid":
                    audit_id(attrValue)
                elif attrName == "lat":
                    audit_lon_lat(attrValue)
                elif attrName == "lon":
                    audit_lon_lat(attrValue)
                else:
                    continue
                
                for i in elem.iter("tag"):
                    if i.attrib["k"] == "addr:street":
                        audit_street_name(i.attrib["v"])
                    #elif i.attrib["k"] == "addr:postcode":
                        #audit_postcode(i.attrib["v"])
                    else:
                        continue

def print_values(ids, loc_values, street_names, postcodes):
    """
    This function labels and prints out bad values for further evaluation on
    how to clean each value or kind of value.
    """
    if len(ids) > 0:
        for n in ids:
            print "Bad id value: " + str(n)
    else:
        print "No bad IDs or UIDs."

    if len(loc_values) > 0:
        for n in loc_values:
            print "Bad location value: " + str(n)
    else:
        print "No bad location values."
    print "Bad street names: \n"
    pprint.pprint(street_names, width=1)
    print "Bad postcodes: \n"
    pprint.pprint(postcodes, width=1)

audit_file(INPUT_FILE)
print_values(bad_ids, bad_loc_values, bad_street_names, bad_postcodes)
