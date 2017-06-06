audit_files.py is used to audit the XML document.

clean_and_prep_files.py cleans relevant data points and writes everything to a csv files.

csv_to_db.py converts all the csv files to a single database file with "maps_data.db" as its default name.

The following are files used or output of scripts but are > 100 mb.
san_francisco.osm is the raw XML file used for this project. I really just want to see how many Starbucks and ice cream shops are in San Francisco.
san_francisco.osm: https://drive.google.com/open?id=0B2BGHnr9cnONSEJYd3FTSEQ2TU0

ways_nodes.csv is the output of clean_and_prep_files.py, storing way nodes data.
way_nodes.csv: https://drive.google.com/open?id=0B2BGHnr9cnONQU1IVEZkQ0RUS0k

nodes.csv is the output of clean_and_prep_files.py, storing nodes data.
nodes.csv: https://drive.google.com/open?id=0B2BGHnr9cnONVXQtOUN4QmtlYTg

maps_data.db is the database filed used to make queries. It is the out put of csv_to_db.py.
maps_data.db: https://drive.google.com/open?id=0B2BGHnr9cnONUmd1Z0xDTWJ6bHc
