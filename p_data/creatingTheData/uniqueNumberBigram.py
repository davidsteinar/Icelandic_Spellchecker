# -*- coding: utf-8 -*-
import pandas as pd
import pickle
from collections import Counter

TrainData = pickle.load(open('risadataframe.p','rb'))

LemmaOrdabok = pickle.load(open('LemmaOrdabok.p','rb'))
LemmaDict = dict(zip(LemmaOrdabok.values, LemmaOrdabok.index.values))

def lemmaindex(string):
    try:
        return LemmaDict[string]
    except:
        return 0

LemmaIndex = TrainData['Lemma'].apply(lemmaindex) #get lemma index from lemmaOrdabok
TrainLemmaArray = LemmaIndex.get_values() 

def pairingfunction(a,b):
    return int( 0.5*(a+b)*(a+b+1)+b )
    
bigrams = []
for x in range(len(TrainLemmaArray)-1):
    i = TrainLemmaArray[x] #index of first word (number)
    j = TrainLemmaArray[x+1] #index of second word (number)
    
    ij = pairingfunction(i,j) #unique combination of i , j (number)
    bigrams.append(ij) 

bicount = Counter(bigrams)
bidict = dict(bicount)
bicountNumber = pd.Series(bidict)

pickle.dump(bicountNumber,open('bicountSeria.p','wb'))


    
