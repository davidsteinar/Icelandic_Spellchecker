# -*- coding: utf-8 -*-

import math
import pandas as pd
import pickle

class ngram(object):
    
    def __init__(self):
        self.allt = pickle.load(open('p_data/allt.p','rb'))

        self.unicount = pickle.load(open('p_data/unicountSeria.p','rb'))
        self.bicount = pickle.load(open('p_data/bicountSeria.p','rb'))
        self.tricount = pickle.load(open('p_data/tricountSeria.p','rb'))
        
        WordOrdabok = pickle.load(open('p_data/WordOrdabok.p','rb'))
        LemmaOrdabok = pickle.load(open('p_data/LemmaOrdabok.p','rb'))
        TagOrdabok = pickle.load(open('p_data/TagOrdabok.p','rb'))
        
        self.WordDict = dict(zip(WordOrdabok.values, WordOrdabok.index.values))
        self.LemmaDict = dict(zip(LemmaOrdabok.values, LemmaOrdabok.index.values))
        self.TagDict = dict(zip(TagOrdabok.values, TagOrdabok.index.values))
        
        self.uniTotal = len(self.unicount)
        self.biTotal  = len(self.bicount)
        self.triTotal = len(self.tricount)

    def getWordProbability(self, word):
        return math.exp(self.Punigram(word))

    def getValue(self, data):
        Tag = list(data["Tag"])
        Lemma = list(data["Lemma"])
        
        b1_logProb = self.Pbigram(Lemma[0], Lemma[1])
        b2_logProb = self.Pbigram(Lemma[1], Lemma[2])
        t_logProb = self.Ptrigram(Tag[0], Tag[1], Tag[2])
        
        return math.exp(b1_logProb + b2_logProb + t_logProb)
    
    def getTagAndLemma(self, word):
        row = self.allt[self.allt["Word"] == word]
        
        if(not pd.isnull(word) and len(row)>0):
            tag = row["Tag"].iloc[0]
            lemma = row["Lemma"].iloc[0]
        else:
            tag = ""
            lemma = ""
        
        return [tag, lemma]
        
    def pairingfunction(self, a,b):
        return int(0.5*(a+b)*(a+b+1)+b)

    def lemmaindex(self, string):
        return self.LemmaDict.get(string, 'Na')
    
    def tagindex(self, string):
        return self.TagDict.get(string, 'Na')
        
    def wordindex(self, string):
        return self.WordDict.get(string, 'Na')
        
    def unigramcount(self, Word):
        try:
            index = self.wordindex(Word)
            return self.unicount[index]
        except:
            return 0
    
    def bigramcount(self, Lemma1, Lemma2):
        try:
            index1 = self.lemmaindex(Lemma1)
            index2 = self.lemmaindex(Lemma2)
            unique = self.pairingfunction(index1,index2)
            count = self.bicount[unique]
            return count
        except:
            return 0
        
    def trigramcount(self, Tag1, Tag2, Tag3):
        try:
            index1 = self.tagindex(Tag1)
            index2 = self.tagindex(Tag2)
            index3 = self.tagindex(Tag3)
            unique12 = self.pairingfunction(index1,index2)
            unique123 = self.pairingfunction(unique12,index3)
            count = self.tricount[unique123]
            return count
        except:
            return 0
            
    def Punigram(self, Word):
        count = self.unigramcount(Word)
        if count == 0:
            logprobability = math.log(1/self.uniTotal)
        else:
            logprobability = math.log(count/self.uniTotal)
        return logprobability
        
    def Pbigram(self, Lemma1, Lemma2):
        count = self.bigramcount(Lemma1,Lemma2)
        if count == 0:
            logprobability = math.log(1/self.biTotal)
        else:
            logprobability = math.log(count/self.biTotal)
        return logprobability
        
    def Ptrigram(self, Tag1, Tag2, Tag3):
        count = self.trigramcount(Tag1,Tag2,Tag3)
        if count == 0:
            logprobability =  math.log(1/self.triTotal)
        else:
            logprobability = math.log(count/self.triTotal)
        return logprobability
