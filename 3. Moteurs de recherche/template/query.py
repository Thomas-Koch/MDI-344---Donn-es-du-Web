#!/usr/bin/env python3

import sqlite3
import re
from math import log
#from shared import extractText, stem
from collections import defaultdict

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# query = input()
# queryWords = [stem(w) for w in query.split()]


for row in cursor.execute("SELECT * FROM inverted_index LIMIT(100)"):
        print(row)

# row = cursor.fetchone()
# row = cursor.fetchall()

