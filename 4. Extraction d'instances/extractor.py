'''Extracts type facts from a wikipedia file
usage: extractor.py wikipedia.txt output.txt

Every line of output.txt contains a fact of the form
    <title> TAB <type>
where <title> is the title of the Wikipedia page, and
<type> is a simple noun (excluding abstract types like
sort, kind, part, form, type, number, ...).

Note: the formatting of the output is already taken care of
by our template, you just have to complete the function
extractType below.

If you do not know the type of an entity, skip the article.
(Public skeleton code)'''

# Inspired from https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/
# and also https://spacy.io/api

from parser import Parser
import sys
import re

import spacy

# loading the model en_core_web_sm of English for vocabluary, syntax & entities
nlp = spacy.load("en_core_web_sm")


if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(-1)

def extractType(content):
    # Code goes here
    bool_return = False
    
    doc = nlp(content)
    for token in doc:
        # produce the lemma for each word we’re analyzing
        if token.lemma_ == 'be':
            bool_return = True
    #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    
        if token.lemma_ == 'mean':
            bool_return = True
            
            
    if bool_return == True:
        for chunk in doc.noun_chunks:
            # The text of the root token’s head.
            tok_head = chunk.root.head.text
            
            # Dependency relation connecting the root to its head.
            tok_dep = chunk.root.dep_
            #print(type(tok_dep))
            
            if (tok_head == 'is' or tok_head == 'are' or tok_head == 'was' or tok_head == 'were' or tok_head == 'means') and (tok_dep == 'attr'):
                #print("###")
                #print(chunk.text,tok_dep)
                #print(chunk.text, chunk.root.text, tok_dep, tok_head)
                return chunk.root.text
    else:
        return None
       

with open(sys.argv[2], 'w', encoding="utf-8") as output:
    for page in Parser(sys.argv[1]):
        typ = extractType(page.content)
        #print(page.title)
        #print(typ)
        if typ:
            output.write(page.title + "\t" + typ + "\n")
            pass

