# -*- coding: utf-8 -*-
import pickle
import math

unicount = pickle.load(open('p_data/unicountSeria.p','rb'))
bicount = pickle.load(open('p_data/bicountSeria.p','rb'))
tricount = pickle.load(open('p_data/tricountSeria.p','rb'))

WordOrdabok = pickle.load(open('p_data/WordOrdabok.p','rb'))
LemmaOrdabok = pickle.load(open('p_data/LemmaOrdabok.p','rb'))
TagOrdabok = pickle.load(open('p_data/TagOrdabok.p','rb'))

WordDict = dict(zip(WordOrdabok.values, WordOrdabok.index.values))
LemmaDict = dict(zip(LemmaOrdabok.values, LemmaOrdabok.index.values))
TagDict = dict(zip(TagOrdabok.values, TagOrdabok.index.values))

total = 143016871

def pairingfunction(a,b):
    return int( 0.5*(a+b)*(a+b+1)+b )

def lemmaindex(string):
    return LemmaDict.get(string, 'Na')

def tagindex(string):
    return TagDict.get(string, 'Na')
    
def wordindex(string):
    return WordDict.get(string, 'Na')
    
def unigramcount(Word):
    try:
        index = wordindex(Word)
        return unicount[index]
    except:
        return 0

def bigramcount(Lemma1,Lemma2):
    try:
        index1 = lemmaindex(Lemma1)
        index2 = lemmaindex(Lemma2)
        unique = pairingfunction(index1,index2)
        count = bicount[unique]
        return count
    except:
        return 0
    
def trigramcount(Tag1,Tag2,Tag3):
    try:
        index1 = tagindex(Tag1)
        index2 = tagindex(Tag2)
        index3 = tagindex(Tag3)
        unique12 = pairingfunction(index1,index2)
        unique123 = pairingfunction(unique12,index3)
        count = tricount[unique123]
        return count
    except:
        return 0
        
def Punigram(Word):
    count = unigramcount(Word)
    if count == 0:
        logprobability = math.log(1/total)
    else:
        logprobability = math.log(count/total)
    return logprobability
    
def Pbigram(Lemma1,Lemma2):
    count = bigramcount(Lemma1,Lemma2)
    if count == 0:
        logprobability = math.log(1/total)
    else:
        logprobability = math.log(count/total)
    return logprobability
    
def Ptrigram(Tag1,Tag2,Tag3):
    count = trigramcount(Tag1,Tag2,Tag3)
    if count == 0:
        logprobability =  math.log(1/total)
    else:
        logprobability = math.log(count/total)
    return logprobability
    
