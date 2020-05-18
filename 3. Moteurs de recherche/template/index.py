#!/usr/bin/env python3

import sqlite3
import re
from math import log
from shared import extractListOfWords, stem, extractText, wordListToFreqDict, sortFreqDict
from collections import defaultdict
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# compute the inverted index and the idf and store them
conn.execute("DROP TABLE IF EXISTS inverted_index")
conn.execute("CREATE TABLE inverted_index (keyword TEXT, URL TEXT, frequency REAL)")


cursor_index = -1
for row in cursor.execute("SELECT * FROM webpages"):
    
    cursor_index = cursor_index + 1
    if (cursor_index % 100 == 0):
        print(cursor_index)
        
        
    list_of_words_stem = list(extractListOfWords(row[0]))
    
    # list_of_words_stem = []
    # for el in list_of_words:
    #     list_of_words_stem.append(stem(el))
    
    dico = wordListToFreqDict(list_of_words_stem)
    # dico = sortFreqDict(dico)
    
    for key, value in dico.items():
        conn.execute('INSERT INTO inverted_index VALUES (?,?,?)', (key, row[1], value/len(list_of_words_stem)))


conn.execute("DROP INDEX IF EXISTS inv_ind")
conn.execute("CREATE INDEX inv_ind ON inverted_index(keyword)")
        
conn.commit()
conn.close()





