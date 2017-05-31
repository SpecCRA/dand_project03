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

Lastly, make a function to write your intended values to a csv file for database
"""

# Alameda de las Pulgas has many variations of capitalizations
alameda_regex = re.compile(r"alameda\sde\slas\pulgas", re.I)

"""
Each dictionary stores corrections to the respective street name, street to replace,
amenity, shop, or cuisine value from the auditing portion.
"""

street_corrections = {
        "Ctr": "Center",
        "Van Ness", "Van Ness Avenue",
         "MILLSBRAE AVE": "Millsbrae Avenue",
         "MacDonald": "MacDonald Ave",
         "Ave": "Avenue",
         "Ave.": "Avenue",
         "Avenie", "Avenue",
         "avenue", "Avenue",
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
        "3605 Telegraph": "3605 Telegraph Avenue",
        "Cesar Chavez St St": "Cesar Chavez Street",
        "Hyde": "Hyde Street",
        "King": "King Street",
        "Vallejo": "Vallejo Street",
        "Alameda De Las": "Alameda de las Pulgas"
        }

amenities_corrections = {}

shops_corrections = {}

cuisine_corrections = {}


def clean_street_names(string):

