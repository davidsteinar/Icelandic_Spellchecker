# -*- coding: utf-8 -*-

import math
import pandas as pd

import ngramchecker

class d(object):
    def __init__(self, data):
        self.data = data.copy().drop_duplicates() #only used for lemma and tag

    def getWordProbability(self, word):
        return math.exp(ngramchecker.Punigram(word))

    def getBigramLogProbability(self, bigram):
        return ngramchecker.Pbigram(bigram[0], bigram[1])
        
    def getTrigramLogProbability(self, trigram):
        return ngramchecker.Ptrigram(trigram[0], trigram[1], trigram[2])

    def getValue(self, data):
        Tag = list(data["Tag"])
        Lemma = list(data["Lemma"])
        
        bigram1 = [Lemma[0], Lemma[1]]
        bigram2 = [Lemma[1], Lemma[2]]
        trigram = [Tag[0], Tag[1], Tag[2]]
        
        b1_logProb = self.getBigramLogProbability(bigram1)
        b2_logProb = self.getBigramLogProbability(bigram2)
        t_logProb = self.getTrigramLogProbability(trigram)
        
        return math.exp(b1_logProb + b2_logProb + t_logProb)
    
    def getTagAndLemma(self, word):
        row = self.data[self.data["Word"] == word]
        
        if(not pd.isnull(word) and len(row)>0):
            tag = row["Tag"].iloc[0]
            lemma = row["Lemma"].iloc[0]
        else:
            tag = ""
            lemma = ""
        
        return [tag, lemma]