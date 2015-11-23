# -*- coding: utf-8 -*-
import pandas as pd
import pickle
from collections import Counter

TrainData = pickle.load(open('risadataframe.p','rb'))

TagOrdabok = pickle.load(open('TagOrdabok.p','rb'))
TagDict = dict(zip(TagOrdabok.values, TagOrdabok.index.values))

def tagindex(string):
    try:
        return TagDict[string]
    except:
        return 0

TagIndex = TrainData['Tag'].apply(tagindex) #get lemma index from lemmaOrdabok
TrainTagArray = TagIndex.get_values() 

def pairingfunction(a,b):
    return int( 0.5*(a+b)*(a+b+1)+b )

trigrams = []
for x in range(len(TrainTagArray)-2):
    i = TrainTagArray[x]
    j = TrainTagArray[x+1]
    k = TrainTagArray[x+2]
    
    ij = pairingfunction(i,j)
    uniqueijk = pairingfunction(ij,k)
    trigrams.append(uniqueijk)

tricount = Counter(trigrams)
tridict = dict(tricount)
tricountNumber = pd.Series(tridict)

pickle.dump(tricountNumber,open('tricountSeria.p','wb'))
    