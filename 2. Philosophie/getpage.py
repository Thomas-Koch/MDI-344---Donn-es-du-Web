#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.parse import unquote
import ssl

# Question 4.1 : gestion du cache
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


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']  # TODO: remplacer ceci
        content = parsed['parse']['text']['*'] # TODO: remplacer ceci 
        return title, content
        
    except KeyError:
        # La page demandée n'existe pas
        return None, None

     

# Questions 4.2, 4.3 et 4.4

def clean_txt(chain) :
    chain = unquote(chain)
    chain = chain.split('#')[0]
    chain = chain.replace('_', ' ')
    return chain



def get_links(page):
    
    title, json_content = getRawPage(page)
    
    soup = BeautifulSoup(json_content, 'html.parser')
    list_div = soup.find('div')
    list_p = list_div.find_all('p', recursive=False)
 
    
    # question 2.4
    links = []
    for link in list_p:
        for el in link.find_all('a'):
            href = el.get('href')
            
            # question 2.5 et 2.6
            if href != None and href[:6] == '/wiki/':
                links.append(href[6:])
                
    # question 2.7       
    return links[:10]



def getPage(page):
    
    # Quesion 4.1 : gestion du cache
    if page in cache.keys() :
        return page, cache[page]

    try :
        title = getRawPage(page)[0]
        content = getRawPage(page)[1]
        
        # On récupère les liens dans la page
        soup = BeautifulSoup(content, 'html.parser')
        soup_div = soup.find('div')
        soup_p = soup_div.findAll('p', recursive=False)
        
        
            
        # question 2.4
        list_href = []
        
        for el in soup_p:
            for link in el.findAll('a'):
                href = link.get('href')
            
                # question 2.5 et 2.6
                if href != None and href[:6] == '/wiki/':
                    list_href.append(href[6:])
        
        
        
        # Questions 4.2, 4.3 et 4.4 : nettoyage des liens
        list_href_clean = []
        for el in list_href:
            if len(clean_txt(el)):
                # on retire si un seul fragment
                list_href_clean.append(clean_txt(el))
               
        # Question 4.5 : on retire les liens vers des pages hors de l’espace de noms principal de Wikipédia
        list_href_clean2 = []
        for el in list_href_clean:
            link_ok = True
            for i in range(len(el)):
                if el[i] == ':' :
                    link_ok = False
                    break
            if link_ok:
            	list_href_clean2.append(el)
           	
        # Question 4.6 : on élimine les doublons
        list_href_clean3 = []
        for el in list_href_clean2:
            if el not in list_href_clean3:
                list_href_clean3.append(el)
                
        # Question 2.7 : on ne garde que les 10 premiers liens
        list_href_clean3 = list_href_clean3[:10]
        
        # Question 4.1 : utilisation du cache
        cache[title] = list_href_clean3
        cache[page] = list_href_clean3
        
        return (title, list_href_clean3)
    
    except :
        return (None, [])
        


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    # print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    print(getPage("Utilisateur:A3nm/INF344"))
    # print(getPage("Histoire"))
    
    # print(getPage("Geoffrey_Midddller"))
    
    # print(get_links(('Utilisateur:A3nm/INF344')))
    

