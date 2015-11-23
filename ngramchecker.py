# -*- coding: utf-8 -*-
import pickle
import math

bicount = pickle.load(open('bicountSeria.p','rb'))
tricount = pickle.load(open('tricountSeria.p','rb'))
LemmaOrdabok = pickle.load(open('LemmaOrdabok.p','rb'))
TagOrdabok = pickle.load(open('TagOrdabok.p','rb'))

LemmaDict = dict(zip(LemmaOrdabok.values, LemmaOrdabok.index.values))
TagDict = dict(zip(TagOrdabok.values, TagOrdabok.index.values))

total = 143016871

def pairingfunction(a,b):
    return int( 0.5*(a+b)*(a+b+1)+b )

def lemmaindex(string):
    return LemmaDict.get(string, 'Na')

def tagindex(string):
    return TagDict.get(string, 'Na')

def bigramflettari(Lemma1,Lemma2):
    try:
        index1 = lemmaindex(Lemma1)
        index2 = lemmaindex(Lemma2)
        unique = pairingfunction(index1,index2)
        count = bicount[unique]
        return count
    except:
        return 0
    
def trigramflettari(Tag1,Tag2,Tag3):
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
    
def Pbigram(Lemma1,Lemma2):
    count = bigramflettari(Lemma1,Lemma2)
    if count == 0:
        logprobability = math.log(1/total)
    else:
        logprobability = math.log(count/total)
    return logprobability
    
def Ptrigram(Tag1,Tag2,Tag3):
    count = trigramflettari(Tag1,Tag2,Tag3)
    if count == 0:
        logprobability =  math.log(1/total)
    else:
        logprobability = math.log(count/total)
    return logprobability
    
