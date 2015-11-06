# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import re
import collections

t079 = open('althingi_text\\079.txt', encoding="utf-8")
tagged079 = pd.read_csv('althingi_tagged\\079.csv')
corrected079 = pd.read_csv('althingi_errors\\079.csv')
text079 = pd.read_table('althingi_text\\079.txt', names=['Speech'])


def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open('althingi_text\\079.txt', encoding="utf-8").read()))
tagged = pd.read_csv('althingi_tagged\\079.csv')

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
 #  splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   for i in range(len(word)+1):
       splits = (word[:1],word[i:])
                  
       for a,b in splits:
           
           for c in alphabet:
               inserts = a + c + b
           
           if len(b)>1:
               transposes = a+b[1]+b[0]+b[2:]
               
           elif b:
               deletes = a+b[1:]
               for c in alphabet:
                   replaces = a + c + b[1:]
               


   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
    
    
    


