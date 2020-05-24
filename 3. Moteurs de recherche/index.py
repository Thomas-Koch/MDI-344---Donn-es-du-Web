#!/usr/bin/env python3

import sqlite3
from math import log
from shared import extractListOfWords, wordListToFreqDict, sortFreqDict


conn = sqlite3.connect('data.db')
cursor_1 = conn.cursor()
cursor_2 = conn.cursor()

# compute the inverted index and the idf and store them

#----------------- INVERTED INDEX -----------------
print("-------- Compute Inverted Index --------")
conn.execute("DROP TABLE IF EXISTS inverted_index")
conn.commit()
conn.execute("CREATE TABLE inverted_index (keyword TEXT, URL TEXT, frequency REAL)")
conn.commit()


cursor_index = -1
for row in cursor_1.execute("SELECT * FROM webpages"):
    
    cursor_index = cursor_index + 1
    if (cursor_index % 100 == 0):
        print(cursor_index, "/ 6400 lines handled")
        
        
    list_of_words_stem = list(extractListOfWords(row[0]))
    
    
    dico = wordListToFreqDict(list_of_words_stem)
    # dico = sortFreqDict(dico)
    
    for key, value in dico.items():
        cursor_2.execute('INSERT INTO inverted_index VALUES (?,?,?)', (key, row[1], value/len(list_of_words_stem)))


conn.execute("DROP INDEX IF EXISTS inv_ind")
conn.commit()
conn.execute("CREATE INDEX inv_ind ON inverted_index(keyword)")
conn.commit()
        

# ----------------- IDF -----------------
print()
print("-------- Compute IDF --------")

conn.execute("DROP TABLE IF EXISTS invert_document_frequency")
conn.commit()
conn.execute("CREATE TABLE invert_document_frequency (keyword TEXT, idf REAL)")
conn.commit()

for row in cursor_1.execute("SELECT COUNT(DISTINCT URL) FROM webpages"):
    nb_urls = row[0]

cursor_index = -1

for row in cursor_1.execute("SELECT keyword, COUNT(URL) FROM inverted_index GROUP BY keyword"):
    
    cursor_index = cursor_index + 1
    if (cursor_index % 10000 == 0):
        print(cursor_index, "/ 240000 lines handled")
    
    cursor_2.execute('INSERT INTO invert_document_frequency VALUES (?,?)', (row[0], log(nb_urls / row[1])))


conn.execute("DROP INDEX IF EXISTS inv_doc_freq")
conn.commit()
conn.execute("CREATE INDEX inv_doc_freq ON invert_document_frequency(keyword)")
conn.commit()

print()
print("Jobs done !")

conn.commit()
conn.close()






