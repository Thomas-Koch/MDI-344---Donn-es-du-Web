#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.parse import unquote
import ssl


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

# Part 2 : Interrogation de l’API Wikipédia
# We compute here a function that return all links contained in an html page

def get_links(page):
    
    title, json = getRawPage(page)
    
    soup = BeautifulSoup(json, 'html.parser')
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
    

    

def getPage(page): # TODO: écrire ceci
    title, json = getRawPage(page)
    
    soup = BeautifulSoup(json, 'html.parser')
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



if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    # print(getPage("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Histoire"))
    # print(getPage("Histoire"))
    
    print(get_links(('Utilisateur:A3nm/INF344')))
    

