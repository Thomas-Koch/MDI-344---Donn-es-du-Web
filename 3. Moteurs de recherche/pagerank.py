import sqlite3
from shared import neighbors, sortFreqDict


conn = sqlite3.connect('data.db')
cursor_1 = conn.cursor()
cursor_2 = conn.cursor()

NB_ITERATIONS = 50
ALPHA = 0.15

# compute and store pagerank

#---------------- COMPUTE ----------------
print("-------- Compute Page Rank --------")

for row in cursor_1.execute("SELECT COUNT(DISTINCT URL) FROM webpages"):
    nb_urls_tot = row[0]

# score = [1/N pour chaque page]
scores_dict = {} 
for row in cursor_1.execute("SELECT URL FROM webpages"):
    scores_dict[row[0]] = 1/nb_urls_tot

new_scores_dict = {} 

for i in range(NB_ITERATIONS):
    
    print('Itération ', i)
    
    for row in cursor_1.execute("SELECT URL FROM webpages"):
        new_scores_dict[row[0]] = 0
    
    # traitons les sauts de page en page
    prob_tel = 0
    list_of_urls_in_page = []
    for row in cursor_1.execute("SELECT URL, content FROM webpages"):
        list_of_urls_in_page = neighbors(row[1], row[0]) 
        
        
        if len(list_of_urls_in_page) > 0 :
            prob_tel += ALPHA * scores_dict[row[0]]
            
            for url in list_of_urls_in_page:
                query_url = (url,)
                cursor_2.execute("SELECT respURL FROM responses WHERE queryURL=?", query_url)
                resp_url = cursor_2.fetchone()[0]
                
                new_scores_dict[resp_url] += scores_dict[row[0]] * (1 - ALPHA) / len(list_of_urls_in_page)
                
        else:
            prob_tel += scores_dict[row[0]]
     
    # traitons les téléportations
    for row in cursor_1.execute("SELECT URL FROM webpages"):
        new_scores_dict[row[0]] += prob_tel / nb_urls_tot
    
    scores_dict = dict.copy(new_scores_dict)


#---------------- STORE ----------------
print()
print("-------- Store Page Rank --------")

conn.execute("DROP TABLE IF EXISTS page_rank")
conn.commit()
conn.execute("CREATE TABLE page_rank (URL TEXT, rank_score REAL)")
conn.commit()

for key, value in scores_dict.items():
    conn.execute('INSERT INTO page_rank VALUES (?,?)', (key, value))
    
conn.commit()
conn.close()

print()
print("Jobs done !")


#---------------- RETURN 20 PAGES WITH BEST PAGERANK ----------------
scores_list_sorted = sortFreqDict(scores_dict)
for i in range(20):
    print(scores_list_sorted[i])





