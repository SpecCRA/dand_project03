#!/usr/bin/env python

import re
import csv
import xml.etree.cElementTree as ET
import pprint

"""
Things I know I need to clean
1. Inconsistent street names - capitalizations, typos, abbreviations
2. Amneties values - different variations for the same amenity, singular/plurals
typos, and capitalizations
3. Shop values - same as amenities
4. Cuisine values - mostly same as amenities and shops, will only take first value
if it has subvalues too
5. Some values need to be removed because of input error and things that just don't 
make sense

Lastly, make a function to write your intended values to a csv file for database
"""

INPUT_FILE = "san_francisco.osm"

# Alameda de las Pulgas has many variations of capitalizations
alameda_regex = re.compile(r"alameda\sde\slas\(pulgas)?", re.I)
# if it matches this, return "Alameda de las Pulgas"

plurals_regex = re.compile(r"")

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
        "pet_store": "pet",
        "pet_supply": "pet",
        "outdoor water sports and swim": "outdoor"
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
        "lao": "laotian"
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
def clean_street_names(string):
    """
    Clean street names with the dictionaries street_corrections and street_replacments.
    Fix capitalizations like all caps and all lower case.
    Fix variations in capitalizations in "Alameda de las Pulgas"
    Things in street_replacements are individually cleaned.
    street_corrections are in the string somewhere.
    -find its location after splitting into a list
    -remove then replace with dictionary value
    Remove "Wedemeyer", looks like it's a typo for Wedemeyer Bakery.
    """
    
    pass

def clean_value(string):
    """
    Takes a string as an argument
    1. makes everything lower case
    2. replaces empty spaces with underscores
    3. removes underscore if it is first character
    4. how do I check for singulars and plurals nicely?
    5. split based on ; and take first value (but not barbecue;korean)
    """
    
    pass

def clean_amenities(string):
    """
    1. Remove addr:housenumber (the value), p, fixme, and yes
    2. lower every string
    3. replace spaces with "_"
    4. split at ";" and only take first value
    5. find singular/plurals and return plurals with plurals regex
    6. use amenities_corretions dictionary for the typos and renaming
    """

    pass
