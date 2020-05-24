#!/usr/bin/env python3

import sqlite3
from shared import stem, sortFreqDict
from collections import defaultdict
import sys

conn = sqlite3.connect('data.db')
cursor_1 = conn.cursor()
cursor_2 = conn.cursor()

# Test pour savoir si le programme est lancé avec arguments
if len(sys.argv) > 1 :
    queryWords = [stem(w) for w in sys.argv[1:] if stem(w) != ""]

else:
    # on prend l'input de la requête
    query = input("Saisissez votre requête :")
    if query == "":
        # si pas de saisie, on utilise une requête type
        query = "comment multiplier des matrices"
    
    queryWords = [stem(w) for w in query.split() if stem(w) != ""]
print()


# compute best query solution and output them
# 2 méthodes possibles : (tf-idf simple) ou (tf-idf * pagerank)

possible_modes = ["tf-idf", "tf-idf * pagerank"]
for mode in possible_modes:
    # création d'un dictionnaire contenant la somme des points par page
    total_point_dict = defaultdict(float)

    for word in queryWords :
        # on va chercher dans le corpus l'idf correspondant au mot recherché
        cursor_1.execute("SELECT keyword, idf FROM invert_document_frequency WHERE keyword = ?", (word,))
        result = cursor_1.fetchone()
        if result != None :
            # le mot est bien dans le corpus
            idf_word = result[1]

            for row in cursor_1.execute("SELECT * FROM inverted_index WHERE keyword = ?", (word,)):
                URL = row[1]
                frequency = row[2]
                if mode == "tf-idf" :
                    total_point_dict[URL] += frequency * idf_word
                elif mode == "tf-idf * pagerank" :
                    # lecture du rank_score de la page
                    cursor_2.execute("SELECT * FROM page_rank WHERE URL = ?", (URL,))
                    rank_score = cursor_2.fetchone()[1] 
                    total_point_dict[URL] += frequency * idf_word * rank_score 
    
    # On peut alors trier les pages selon leur total de points en décroissant
    #---------------- RETURN 10 PAGES WITH BEST SCORES ----------------
    url_sorted = sortFreqDict(total_point_dict)
    
    print("Résultat de votre reqûete avec le mode", mode, ".")
    print()
    
    for i in range(1, 11):
        print("Rang n°", i, " : " , url_sorted[i-1][1])
    
    print()
    print()


conn.close()

