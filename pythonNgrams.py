# -*- coding: utf-8 -*-
import pandas as pd
import os
import pickle
from nltk.util import ngrams
from collections import Counter


def bigram(Lemma):
    bigrams = ngrams(list(Lemma),2)
    bigramscount = Counter(list(bigrams))
    return bigramscount
    
def trigram(Tag):
    trigrams = ngrams(list(Tag),3)
    trigramscount = Counter(list(trigrams))
    return trigramscount

finalbigram  = Counter()
finaltrigram = Counter()

for i in os.listdir(os.getcwd()+'\\althingi_tagged'):
  
    t = pd.read_csv('althingi_tagged\\'+i)
    t = t.fillna('')
    
    tLemma = t['Lemma']
    tTag   = t['Tag']
    
    tbigramcount  = bigram(list(tLemma))
    ttrigramcount = trigram(list(tTag))
    
    finalbigram = finalbigram + tbigramcount
    finaltrigram = finaltrigram + ttrigramcount
    

pickle.dump(finalbigram,open('finalbigrams.p','wb'))
pickle.dump(finaltrigram,open('finaltrigrams.p','wb'))

wordlemmadict = dict(zip(t.Word))



''' breyta indexi hjá orði í binary ,  AND tvö orð saman og telja síðan 

#df = pd.DataFrame.from_dict(d, orient='index').reset_index()
    
    
    

#example bigramscount['að','vera']
#example bigramscount.most_common(4)

