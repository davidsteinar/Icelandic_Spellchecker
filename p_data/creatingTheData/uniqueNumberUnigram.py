# -*- coding: utf-8 -*-
import pandas as pd
import pickle
from collections import Counter

TrainData = pickle.load(open('risadataframe.p','rb'))

WordOrdabok = pickle.load(open('WordOrdabok.p','rb'))
WordDict = dict(zip(WordOrdabok.values, WordOrdabok.index.values))

def wordindex(string):
    try:
        return WordDict[string]
    except:
        return 0

WordIndex = TrainData['Word'].apply(wordindex) #get word index from lemmaOrdabok
TrainWordArray = WordIndex.get_values() 

unicount = Counter(TrainWordArray)
unidict = dict(unicount)
unicountNumber = pd.Series(unidict)

pickle.dump(unicountNumber,open('unicountSeria.p','wb'))


