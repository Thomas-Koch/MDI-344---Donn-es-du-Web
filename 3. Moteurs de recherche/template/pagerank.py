import sqlite3
import re
from math import log
from shared import extractText, neighbors
from collections import defaultdict


NB_ITERATIONS = 50
ALPHA = 0.15

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

#compute and store pagerank

conn.commit()

    
# score = [ 1/n pour chaque page]

# pour chaque itération:
# 	nouveau_score = [ 0 pour chaque page ]
# 	proba_téléportation = 0

#         // traitons les sauts de page en page
# 	pour chaque page P:
# 		s'il y a des liens sur P:
# 			proba_téléportation += α × score[P]
# 			pour chaque lien de P vers P' :
# 				nouveau_score[P'] += score[P] × (1-α) / nombre de liens sur P
# 				
# 		s'il n'y a pas de lien sur P:
# 			proba_téléportation += score[P]


#         // traitons les téléportations
# 	pour chaque page P:
#                 nouveau_score[P] += proba_téléportation / nombre de pages