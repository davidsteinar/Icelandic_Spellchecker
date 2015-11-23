# -*- coding: utf-8 -*-
import pandas as pd
import os
import pickle

def uniquedict(df , column):
    c = str(column)
    unique = df.drop_duplicates(subset = c)
    unique = unique[c]
    unique = unique.order()
    unique = unique.reset_index(drop=True)
    return unique

allt = pd.DataFrame(columns = ['Word','Tag','Lemma'])

for i in os.listdir(os.getcwd()+'\\althingi_tagged'):
    temp = pd.read_csv('althingi_tagged\\'+i)
    temp = temp.fillna(' ')
    allt = allt.append(temp)
    
    
LemmaOrdabok = uniquedict(allt,'Lemma')
TagOrdabok = uniquedict(allt,'Tag')
WordOrdabok = uniquedict(allt,'Word')

pickle.dump(LemmaOrdabok,open('LemmaOrdabok.p','wb'))
pickle.dump(TagOrdabok,open('TagOrdabok.p','wb'))
pickle.dump(WordOrdabok,open('WordOrdabok.p','wb'))