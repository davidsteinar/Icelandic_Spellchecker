# -*- coding: utf-8 -*-

import pandas as pd

alphabet = "aábcdðeéfghiíjklmnoópqrstuúvxyýzþæö"

#TODO: change number
edit1Weight = 0.894
edit2Weight = 0.092

def getEdits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def getEdits2(word):
    return set(e2 for e1 in getEdits1(word) for e2 in getEdits1(e1))

def removeUnknown(words, d): 
    return set(w for w in words if d.getWordProbability(w)>1e-6) #TODO: change number

def getPossibleWords(word, d):
    edit1 = removeUnknown(getEdits1(word), d)
    list1 = []
    for i in edit1:
        list1.append([i, edit1Weight])
    df1 = pd.DataFrame(list1, columns = ["Word", "Weight"])
    
    """edit2 = removeUnknown(getEdits2(word), d)
    list2 = []
    for i in edit2:
        list2.append([i, edit2Weight])
    df2 = pd.DataFrame(list2, columns = ["Word", "Weight"])
    
    df = pd.concat([df1, df2], ignore_index=True)"""
    df = df1
    return df