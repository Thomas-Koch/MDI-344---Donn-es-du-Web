#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
import ssl
from urllib.parse import unquote


# Q 4.1
global cache
cache = dict()

def getJSON(page):
    params = urlencode({
      'format': 'json',  # TODO: compléter ceci
      'action': 'parse',  # TODO: compléter ceci
      'prop': 'text',  # TODO: compléter ceci
      'redirects': 'true',  # TODO: compléter ceci
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')

# Q 4.2, 4.3 et 4.4
def cleaning(valeur) :
    valeur = unquote(valeur)
    valeur = valeur.split('#')[0]
    valeur = valeur.replace('_', ' ')
    return valeur


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']  # TODO: remplacer ceci
        content = parsed['parse']['text']['*']  # TODO: remplacer ceci
        return title, content
    
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    #pass  # TODO: écrire ceci
    
    # Q 4.1 gestion d'un cache
    if page in cache.keys() :
        return page, cache[page]
    
    try :
        title = getRawPage(page)[0]    
        content = getRawPage(page)[1]
       
        
        # récupère les liens d'une page
        soup = BeautifulSoup(content, 'html.parser')
        soup = soup.find('div')
    
        liste_href = []
        # Q 2.4
        for el in soup.findAll('p', recursive = False) :
            for lien in el.findAll('a') :
                href = lien.get('href')
                
                #liste_href.append(href)
                # Q 2.5 + 2.6
                if href != None and href[:6] == '/wiki/' :
                    liste_href.append(href[6:])
        
        # cleaning des liens Q 4.2, 4.3 et 4.4
        liste_href_clean = []
        for el in liste_href:
            if len(cleaning(el)): # Q 4.3 on retire si juste un fragment
                liste_href_clean.append(cleaning(el))
        
        # Q 4.5 
        # retirer les liens hors de l’espace de noms principal de Wikipédia
        liste_href_clean2 = [] 
        for el in liste_href_clean:
            lien_ok = True
            for j in range(len(el)):
                if el[j] ==':':
                    lien_ok = False
                    break
            if lien_ok:
                liste_href_clean2.append(el)
        
        # Q 4.6 éliminer les doublons
        liste_href_clean3 = [] 
        for el in liste_href_clean2:
            if el not in liste_href_clean3:
                liste_href_clean3.append(el)
        
        # Q 2.7 on ne garde que 10 liens au max
        liste_href_clean3 = liste_href_clean3[:10]
        
        # Q 4.1 on met les 2 en cache au cas où
        cache[title] = liste_href_clean3
        cache[page] = liste_href_clean3
        
        return (title,liste_href_clean3)

    except :
        return (None, [])





if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    #print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    #print(getPage("Histoire"))
    print(getPage("Utilisateur:A3nm/INF344"))
    
    # print(getPage("Histoire"))
    
    # print(getPage("Geoffrey_Midddller"))
   
