#!/usr/bin/env python

import re
import csv
import xml.etree.cElementTree as ET
import pprint

INPUT_FILE = "san_francisco.osm"

# Alameda de las Pulgas has many variations of capitalizations
alameda_regex = re.compile(r"(alameda\sde\sla\s)(pulgas)?", re.I)
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

def clean_value(string):
    """
    Takes a string as an argument
    1. makes everything lower case
    2. replaces empty spaces with underscores
    3. how do I check for singulars and plurals nicely?
    4. split based on ; and take first value (but not barbecue;korean)
    5. also split on , and take first value

    This function deals with amenity, shop, and cuisine values.
    """
    working_string = string.lower()
    
    if " " in working_string:
        working_string = working_string.replace(" ", "_")

    if ";" in working_string and not "barebecue;korean": #special case 
        working_string = working_string.split(";")[0]
    if "," in working_string:
        working_string = working_string.split(",")[0]

    return working_string

def clean_amenity_value(string):
    """
    1. Remove addr:housenumber (the value), p, fixme, and yes -- return None
    2. use amenities_corretions dictionary for the typos and renaming
    """
    string = clean_value(string)
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
    new_string = clean_value(string)
    if new_string in corrections_dict.keys():
        return corrections_dict[new_string]
    else:
        return new_string

def shape_element():
    pass

def write_to_csv():
    pass
