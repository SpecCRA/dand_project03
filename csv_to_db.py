#!/usr/bin/env python

"""
This file writes my csv files into database files
"""

import sqlite3
import csv
from pprint import pprint

sqlite_file = "map_data.db"
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

def add_table(add_table_query):
    cur.execute(add_table_query)
    conn.commit()

# Each of these are the table creation queries from data_wrangling_schema.sql
add_nodes = "CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL,lat REAL,lon REAL,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT)"

add_nodes_tags = "CREATE TABLE nodes_tags (id INTEGER,key TEXT,value TEXT,type TEXT,FOREIGN KEY (id) REFERENCES nodes(id))"

add_ways = "CREATE TABLE ways (id INTEGER PRIMARY KEY NOT NULL,user TEXT,uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT)"

add_ways_tags = "CREATE TABLE ways_tags (id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,type TEXT,FOREIGN KEY (id) REFERENCES ways(id))"

add_ways_nodes = "CREATE TABLE ways_nodes (id INTEGER NOT NULL,node_id INTEGER NOT NULL,position INTEGER NOT NULL,FOREIGN KEY (id) REFERENCES ways(id),FOREIGN KEY (node_id) REFERENCES nodes(id))"

# drop tables I want to write if they exist right now
cur.execute("""DROP TABLE IF EXISTS nodes_tags""")
cur.execute("""DROP TABLE IF EXISTS nodes""")
cur.execute("""DROP TABLE IF EXISTS ways""")
cur.execute("""DROP TABLE IF EXISTS ways_tags""")
cur.execute("""DROP TABLE IF EXISTS ways_nodes""")
conn.commit()

add_table(add_nodes)
add_table(add_nodes_tags)
add_table(add_ways)
add_table(add_ways_tags)
add_table(add_ways_nodes)

with open ("nodes_tags.csv", "rb") as fin:
    dr = csv.DictReader(fin)
    node_tags_db = [(i['id'].decode("utf-8"), i['key'].decode("utf-8"), i['value'].decode("utf-8"), i['type'].decode("utf-8")) for i in dr]

cur.executemany("INSERT INTO nodes_tags(id, key, value, type) VALUES (?, ?, ?, ?);", node_tags_db)
conn.commit()

#cur.execute("SELECT * FROM nodes_tags")
#all_rows = cur.fetchall()
#print ('1):')
#pprint (all_rows)

conn.close()

