# -*- coding: utf-8 -*-
import pandas as pd
from nltk.util import ngrams
from nltk.metrics import edit_distance
from collections import Counter

tagged079 = pd.read_csv('althingi_tagged\\080.csv')
t079 = tagged079.fillna('')

Words = t079['Word']
Lemma = t079['Lemma']
Tagg  = t079['Tag']

wordscount = Counter(list(Words))

bigrams = ngrams(list(Lemma),2)
bigramscount = Counter(list(bigrams))

trigrams = ngrams(list(Tagg),3)
trigramscount = Counter(list(trigrams))



#example bigramscount['að','vera']

