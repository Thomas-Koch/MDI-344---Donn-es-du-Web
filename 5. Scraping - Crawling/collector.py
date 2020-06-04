# -*- coding: utf-8 -*-
# écrit par Jean-Claude Moissinac, structure du code par Julien Romero

from sys import argv
import sys
import urllib
from bs4 import BeautifulSoup
import time
import re

if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode

class Collecte:
    """pour pratiquer plusieurs méthodes de collecte de données"""

    def __init__(self):
        """__init__
        Initialise la session de collecte
        :return: Object of class Collecte
        """
        # DO NOT MODIFY
        self.basename = "collecte.step"
        self.name = "tkoch"

    def collectes(self):
        """collectes
        Plusieurs étapes de collectes. VOTRE CODE VA VENIR CI-DESSOUS
        COMPLETER les méthodes stepX.
        """
        self.step0()
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()

    def step0(self):
        # cette étape ne sert qu'à valider que tout est en ordre; rien à coder
        stepfilename = self.basename+"0"
        print("Comment :=>> Validation de la configuration")
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(self.name)
        
    def step1(self):
        stepfilename = self.basename+"1"
        result = ""
        # votre code ici
        url = "http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&query_txt=video&submit=&patents=on"
        rqst = urllib.request.Request(url)
        
        with urllib.request.urlopen(rqst) as resp:
            result = str(resp.read())
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
    def step2(self):
        stepfilename = self.basename+"2"
        result = ""
        # votre code ici
        
        links = []
        resfile = open(self.basename+"1", 'r').read()
        soup = BeautifulSoup(resfile, 'html.parser')
        
        for link in soup.findAll('a'):
            link_href = link.get('href')
            links.append(str(link_href))
        
        result = "\n".join(links)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
    def linksfilter(self, links):
        # flinks = links
        # votre code ici
        links = sorted(set(links))
        
        to_remove = ['/', '/services.html', '/contact.html', '/privacy.html',
                    '/register.html', '/tools-resources.html', 
                    'https://twitter.com/FPOCommunity', 
                    'http://www.linkedin.com/groups/FPO-Community-4524797', 
                    'http://www.sumobrainsolutions.com/', 'None']
        
        flinks = [] 
        
        for el in links :
            if not (el in to_remove) and not (el.startswith("\\'result.html")) \
                                    and not (el.startswith('http://research')) \
                                    and not (el.startswith('/search.html')) :
                flinks.append(el)
        # print(flinks)
        return flinks
        
    def step3(self):
        stepfilename = self.basename+"3"
        result = ""
        # votre code ici
        result = self.linksfilter(open(self.basename+"2", 'r').read().splitlines())
        print("------- Step 3 -------")
        print("Il y a ", len(result), " liens filtrés dans la liste.")
        
        result = "\n".join(result)
        # print(result)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
            
        return result
        
    def step4(self):
        stepfilename = self.basename+"4"
        result = ""
        # votre code ici
        res_open_step3 = open(self.basename+"3", 'r', encoding="utf-8").read().splitlines()
        resfile = list(res_open_step3)[:10]
        
        result = []
        for link in resfile:
            rqst = urllib.request.Request('http://www.freepatentsonline.com/' + str(link))
            
            with urllib.request.urlopen(rqst) as resp:
                res = str(resp.read())
            
            soup = BeautifulSoup(res, 'html.parser')
            
            links = []
            
            for link in soup.findAll('a'):
                link_href = link.get('href')
                links.append(str(link_href))
            
            res = "\n".join(self.linksfilter(links))
            
            result.append(res)
            
            time.sleep(2)
        
        result = sorted(set(result))
        result = "\n".join(result)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
        result_step4 = open(self.basename+"4", 'r').read().splitlines()
        print("------- Step 4 -------")
        print("Il y a ", len(result_step4), " liens filtrés dans la liste.")
        
        
    def contentfilter(self, link):
        soup = BeautifulSoup(link, 'html.parser')
        
        inventors = soup.find_all(text=re.compile('Inventors:'))
        title = soup.find_all(text=re.compile('Title:'))
        application_num = soup.find_all(text=re.compile('Application Number:'))
        
        if inventors is not None or title is not None or application_num is not None:
            return True
        else:
            return False
    
    def contentfilter2(self, res):
        soup = BeautifulSoup(res, 'html.parser')
            
        for div in soup.findAll('div'):
            inventors = soup.find_all(text=re.compile('Inventors:'))
            title = soup.find_all(text=re.compile('Title:'))
            application_num = soup.find_all(text=re.compile('Application Number:'))
                
            if inventors is not None or title is not None or application_num is not None:
                return True
            else:
                return False
                
                
    def step5(self):
        stepfilename = self.basename+"5"
        result = ""
        # votre code ici
        list_links = []
        list_links_step4 = list(open(self.basename+"4", 'r', encoding="utf-8").read().splitlines())

        list_html_links = []
        for el in list_links_step4:
            if el.endswith('html'):
                list_html_links.append(el)
        list_html_links = sorted(list_html_links)
        
        for link in list_html_links:
            
            if len(list_links) > 10:
                break
            
            rqst = urllib.request.Request('http://www.freepatentsonline.com' + str(link))
            with urllib.request.urlopen(rqst) as resp:
                res = str(resp.read())
            
            if self.contentfilter2(res) == True:
                list_links.append(link)
                list_links = list(set(list_links))
                    
                if len(list_links) > 10:
                    break
                
        list_links = sorted(set(list_links))[:10]
        result = "\n".join(list_links)
        
        print("------- Step 5 -------")
        print("Il y a ", len(list_links), " liens filtrés dans la liste.")

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
    
    def step6(self):
        stepfilename = self.basename+"6"
        result = ""
        # votre code ici
        
        list_links_step5 = list(open(self.basename+"5", 'r', encoding='utf-8').read().splitlines())[:5]
        
        inventorlist = []
        
        for link in list_links_step5:
            
            rqst = urllib.request.Request('http://www.freepatentsonline.com' + str(link))
            with urllib.request.urlopen(rqst) as resp:
                res = (resp.read()).decode('utf-8')
                
            soup = BeautifulSoup(res, 'html.parser')
            
            inventors = soup.find_all(text=re.compile('Inventors:'))
            
            divs = [inventor.parent.parent for inventor in inventors]
            for d in divs[0].descendants:
                if d.name == 'div' and d.get('class', '') == ['disp_elm_text']:
                    inventorlist.append(d.text)
        
        result = "\n".join(inventorlist)
        print("------- Step 5 -------\n")
        print("Inventeurs trouvés : \n")
        print(result)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
if __name__ == "__main__":
    collecte = Collecte()
    collecte.collectes()
