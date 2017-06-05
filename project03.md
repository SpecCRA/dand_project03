#OpenStreetMap Data Case Study
---
##Map Area
###San Francisco, CA
*[OpenStreetMap link](https://www.openstreetmap.org/relation/111968)
*[Direct link to my file](https://drive.google.com/open?id=0B2BGHnr9cnONSEJYd3FTSEQ2TU0)

This is a map of my foggy home city. It also includes bits of the surrounding areas such as Berkeley and Daly City. I'm mostly interested in the shop and amenities queries... like how many ice cream shops are in San Francisco.

##Problems Encountered in Map Data
After a very long auditing process on the large XML document, here are the major problems I noticed:
*Inconsistent street name abbreviations (ST, St., St for Street)
*Incomplete entries ("Telegraph" for "Telegraph Avenue")
*Inconsistent zip codes (CA 94116)
*Inconsistent shop, amenity, and cusiine values (typos, singulars/plurals)
*Many shop and cuisine values are referring to the same thing (Hair Salon, hair salon, hair_salon, hairdresser)
*Values in every audited category had inconsistent capitalizaions 

##Cleaning Street Names