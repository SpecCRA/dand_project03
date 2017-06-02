#!/usr/bin/env python

import re
import csv
import xml.etree.cElementTree as ET
import pprint

INPUT_FILE = "san_francisco.osm"

# Alameda de las Pulgas has many variations of capitalizations
alameda_regex = re.compile(r"(alameda\sde\sla\s)(pulgas)?", re.I)
# This is the same as the regex in the quizzes except I removed #
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%$@\,\. \t\r\n]')

"""
Each dictionary stores corrections to the respective street name, street to replace,
amenity, shop, or cuisine value from the auditing portion.
"""

street_corrections = {
        "Ctr": "Center",
        "Ave": "Avenue",
        "Ave.": "Avenue",
        "Avenie": "Avenue",
        "avenue": "Avenue",
        "Blvd": "Boulevard",
        "Blvd.": "Boulevard",
        "Dr": "Drive",
        "Dr.": "Drive",
        "Hwy": "Highway",
        "street": "Street",
        "St": "Street",
        "St.": "Street",
        "Plz": "Plaza"
         }

street_replacements = {
        "Van Ness": "Van Ness Avenue",
        "MILLSBRAE AVE": "Millsbrae Avenue",
        "MacDonald": "MacDonald Avenue",
        "3605 Telegraph": "3605 Telegraph Avenue",
        "Cesar Chavez St St": "Cesar Chavez Street",
        "Hyde": "Hyde Street",
        "King": "King Street",
        "Vallejo": "Vallejo Street",
        "broadway": "Broadway",
        "townsend street": "Townsend Street",
        "New Montgomery": "New Montgomery Street"
        }

amenities_corrections = {
        "car_sharing": "car_share",
        "community_centre": "community_center",
        "dancing_school": "dance_school",
        "fountian": "fountain" 
        }

shops_corrections = {
        "hairdresser": "hair_salon",
        "nail_salon": "nails",
        "bail_service": "bail_bond",
        "clothing": "clothes",
        "confectionary": "confectionery",
        "herbalist": "herbs",
        "herb": "herbs",
        "pet_store": "pet",
        "pet_supply": "pet",
        "outdoor_water_sports_and_swim": "outdoor",
        "beauty_products": "beauty",
        "fishing": "fish",
        "floor": "flooring",
        "garden_centre": "garden_center",
        "framing": "frame",
        "pawn": "pawnbroker",
        "thift_store": "thrift",
        "appliance": "appliances",
        "bathroom_furnishing": "bathroom_furnishings",
        "craft": "crafts",
        "rug": "rugs",
        "sport": "sports",
        "vitamin": "vitamins"
        }

cuisines_corrections = {
        "subs/sandwiches": "sandwiches",
        "dimsum": "dim_sum",
        "coffee1": "coffee",
        "coffee_shop": "coffee",
        "bubble_tea": "boba",
        "korean_food": "korean",
        "vietnamnese": "vietnamese", 
        "bbq": "barbecue",
        "doughnut": "donuts",
        "lao": "laotian",
        "california": "californian",
        "homemade_ice_cream": "ice_cream",
        "frozen_yoghurt": "frozen_yogurt",
        "guatamalen": "guatamalan",
        "hawaian": "hawaiian",
        "mexican_food": "mexican",
        "burger": "burgers",
        "burittos": "burrito",
        "crepe": "crepes",
        "donut": "donuts",
        "donut_shop": "donuts",
        "hot_dog": "hot_dogs",
        "hotdog": "hot_dogs",
        "noodle": "noodles",
        "salad": "salads",
        "sandwich": "sandwiches",
        "smoothie": "smoothies",
        "soup": "soups",
        "taco": "tacos"
        }

direction_storage = {
        "N": "North",
        "S": "South",
        "E": "East",
        "W": "West",
        "NE": "Northeast",
        "NW": "Northwest",
        "SE": "Southeast",
        "SW": "Southwest"
        }

"""
When creating your function to clean files, make sure you write in these steps.
1. Lower strings so everything is lower case
2. Replace all spaces with underscores
3. Check for special cases
4. Check to see if you need to convert to plurals
5. Check for special cases to skip or replace
6. Then check in dictionaries for each case
7. Remember with subcategories, just take the first one (split on ;)
"""

def clean_abbrev(string):
    """
    Checks and replaces a string for street or directional abbreviations with its
    full name. Its purpose is to give the street names consistency. 
    This function is specifically for street names and nothing else.
    """

    words = string.split()
    for word in words:
        if word in street_corrections.keys():
            pos = words.index(word)
            words[pos] = street_corrections[word]
            string = " ".join(words)
            return string
        elif word in direction_storage.keys() and not string == "Avenue E":
            pos = words.index(word)
            words[pos] = direction_storage[word]
            string = " ".join(words)
            return string

def clean_street_name(string):
    """
    Clean street names with the dictionaries street_corrections and street_replacments.
    Fix variations in capitalizations in "Alameda de las Pulgas"
    Things in street_replacements are individually cleaned.
    street_corrections are in the string somewhere.
    -find its location after splitting into a list
    -remove then replace with dictionary value
    Remove "Wedemeyer", looks like it's a typo for Wedemeyer Bakery.
    """
    words = string.split()
    if string in street_replacements.keys():
        string = string_replacements[string]
        return string
    elif alameda_regex.search(string):
        string = "Alameda de las Pulgas"
        return string
    elif string == "Wedemeyer":
        pass
    else:
        try:
            clean_abbrev(string)
        except:
            return string

def prep_value(string):
    """
    Takes a string as an argument
    1. makes everything lower case
    2. replaces empty spaces with underscores
    3. split based on ; and take first value (but not barbecue;korean)
    4. also split on , and take first value

    This function deals with amenity, shop, and cuisine values.
    """
    working_string = string.lower()
    
    if " " in working_string:
        working_string = working_string.replace(" ", "_")

    elif ";" in working_string and not "barebecue;korean": #special case 
        working_string = working_string.split(";")[0]
    elif "," in working_string:
        working_string = working_string.split(",")[0]

    return working_string

def clean_amenity_value(string):
    """
    1. Remove addr:housenumber (the value), p, fixme, and yes -- return None
    2. use amenities_corretions dictionary for the typos and renaming
    """
    string = prep_value(string)
    if string == "addr:housenumber" or string == "p" or string == "fixme" \
            or string == "yes":
                return None
    else:
        try:
            if string in amenities_corrections.keys():
                return amenities_corrections[string]
        except:
            return string

def clean_shop_cuisine(corrections_dict, string):
    """
    This is used for shop and cuisine values. The methods to clean these values
    are the same. First it calls the clean_value function and checks to see if
    there are corrections to be made. If not, this function will just return the
    original string.
    """
    new_string = prep_value(string)
    if new_string in corrections_dict.keys():
        return corrections_dict[new_string]
    else:
        return new_string

def process_key(key_string):
    if ":" in key_string:
        indexed_string = key_string.find(":")
        tag_type = key_string[:indexed_string]
        new_key = key_string[indexed_string+1]
        return [new_key, tag_type]
    else: 
        new_key = key_string
        tag_type = "regular"
        return [new_key, tag_type]

def shape_element(filename):

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':

      # first loop through to get node's attributes and values into a dictinonary
        for attrName, attrValue in element.attrib.items():
            if attrName in NODE_FIELDS:
                node_attribs[attrName] = attrValue
        #print node_attribs

        """ 
        Next, loop through the child tags and parse out the
        key, value, and clean up the 'key' to create types. Then
        put everything into a dictionary to append to tags list.
        """
        for i in element.iter('tag'):
            #print i
            temp_dict = {}
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            else:
                temp_dict['id'] = element.attrib['id']
                temp_dict['key'] = process_key(i.attrib['k'])[0]
                temp_dict['type'] = process_key(i.attrib['k'])[1]
                temp_dict['value'] = i.attrib['v']
                #print temp_dict
            tags.append(temp_dict)
        #print tags

        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':

        for attrName, attrValue in element.attrib.items():
            if attrName in WAY_FIELDS:
                #print attrName
                #print attrValue
                way_attribs[attrName] = attrValue
        #print way_attribs

        """ 
        Since the way tags follow the same rules as the node tags, these
        are processed the same way.
        """
        for i in element.iter('tag'):
            temp_dict = {}
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            else:
                temp_dict['id'] = element.attrib['id']
                temp_dict['key'] = process_key(i.attrib['k'])[0]
                temp_dict['type'] = process_key(i.attrib['k'])[1]
                temp_dict['value'] = i.attrib['v']
            tags.append(temp_dict)
        print tags

        """
        enumerate() is used here to create a counter for each 'nd' child node.
        """

        for counter, i in enumerate(element.iter('nd')):
            temp_dict = {}
            temp_dict['id'] = element.attrib['id']
            temp_dict['node_id'] = i.attrib['ref']
            temp_dict['position'] = counter
            way_nodes.append(temp_dict)
        #print way_nodes

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

def write_to_csv():
    pass
