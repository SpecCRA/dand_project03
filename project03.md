# San Francisco OpenStreetMap Data Case Study
---
## Map Area
### San Francisco, CA
  * [OpenStreetMap link](https://www.openstreetmap.org/relation/111968)
  * [Direct link to my file](https://drive.google.com/open?id=0B2BGHnr9cnONSEJYd3FTSEQ2TU0)

This is a map of my foggy home city. It also includes bits of the surrounding areas such as Berkeley and Daly City. I'm mostly interested in the shop and amenities queries... like how many ice cream shops are in San Francisco.

## Problems Encountered in Map Data
After a very long auditing process on the large XML document, here are the major problems I noticed:
  * Inconsistent street name abbreviations (ST, St., St for Street)
  * Incomplete entries ("Telegraph" for "Telegraph Avenue")
  * Inconsistent zip codes (CA 94116)
  * Inconsistent shop, amenity, and cusiine values (typos, singulars/plurals)
  * Many shop and cuisine values are referring to the same thing (Hair Salon, hair salon, hair_salon, hairdresser)
  * Values in every audited category had inconsistent capitalizaions 

## Problems in Street Names
To audit street names, I first compiled a list of expected street names. Then I checked the last word of every street name to see if it was in the list. If there were many entries that aren't in the list, then I must have missed it. Otherwise, I made a note on problems to clean later. 

Variations of "Alameda de las Pulgas" were found through a regex search.

```alameda_regex = re.compile(r"(alameda\sde\sla\s)(pulgas)?", re.I)```

To clean the street names, I either replaced the entire street name or replaced parts of the string with the correct abbreviations.

## Problems in Amenity, Shop, and Cuisine Values
The main problem with these values is many of them are two values that refer to the same thing. Some are named vaguely or different such as "dimsum" and "dim_sum" or variations of singular and plural versions of the word. I also made notes of typos and removed subcategories to further simplify categorizing this data.

I made dictionaries to replace all the "bad" values to have a more consistent query for the same values. Some bad values that are mislabeled are removed.