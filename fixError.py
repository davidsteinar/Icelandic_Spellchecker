# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

minNonWordProb = 1e-5
minRealWordProb = 1.84e-19

alphabet = "aábdðeéfghiíjklmnoópqrstuúvxyýþæöAÁBDEÉFGHIÍJKLMNOÓPQRTSTUÚVYÝÞÆÖ"

edit1Weight = 0.894
edit2Weight = 1-edit1Weight #0.092

minKnownWordProb = 6.15e-06

def nonWord(data, ngram):
    for i in range(0, len(data)):
        word_ = data["Word"][i]
        value_ = ngram.getWordProbability(word_)
        if((not pd.isnull(word_)) and ("." not in word_) and (value_<minNonWordProb)):
            data["CorrectWord"][i] = getCorrectNonWord(word_, ngram)
        else:
            data["CorrectWord"][i] = word_ 
    
    return data

def getCorrectNonWord(word, ngram):
    possible = getPossibleWords(word, ngram)
    possible["Probability"] = 0
    
    for i in range(0, len(possible)):
        weight_ = possible["Weight"][i]
        word_ = possible["Word"][i]
        probability_ = ngram.getWordProbability(word_)
        possible.loc[i, "Probability"] = weight_*probability_
    
    if(len(possible)>0):
        idMax = possible["Probability"].idxmax()
        return possible["Word"].iloc[idMax]
    else:
        return word

def realWord(data, ngram):
    data = addNanRows(data)
    
    for i in range(1, len(data)-1):
        data_ = data[i-1:i+2]
        word_ = data["Word"][i]
        value_ = ngram.getValue(data_)
        if(not pd.isnull(word_) and ("." not in word_) and value_<minRealWordProb):
            data["CorrectWord"][i] = getCorrectRealWord(data_, ngram)
    
    #removing the top and bottom NaN row we added earlier
    data = data[1:len(data)-1]
    return data.reset_index(drop=True)

def addNanRows(data):
    newData = pd.DataFrame(columns=data.columns)
    newData.loc[0] = np.nan
    newData = newData.append(data, ignore_index=True)
    newData.loc[len(newData)] = np.nan
    return newData

def getCorrectRealWord(data, ngram):
    data = data.reset_index(drop=True)
    word = data["Word"][1]

    #adding the current word to the top of the list in case all possibilities
    #are equally probable we choose the old one
    df1 = pd.DataFrame([[word, edit1Weight]], columns=["Word", "Weight"]) 
    df2 =  getPossibleWords(word, ngram)
    possible = pd.concat([df1, df2], ignore_index=True)
    possible["Probability"] = 0
    
    data = updateTrigramLemmaAndTag(data, data["CorrectWord"][0], 0, ngram)
    data = updateTrigramLemmaAndTag(data, data["CorrectWord"][2], 2, ngram)
    
    for i in range(0, len(possible)):
        weight_ = possible["Weight"][i]
        data_ = updateTrigramLemmaAndTag(data, possible["Word"][i], 1, ngram)
        probability_ = ngram.getValue(data_)
        possible.loc[i, "Probability"] = weight_*probability_
    
    if(len(possible)>0):
        idMax = possible["Probability"].idxmax()
        return possible["Word"].iloc[idMax]
    else:
        return word

def updateTrigramLemmaAndTag(data, newWord, i, ngram):
    if(not pd.isnull(newWord) and newWord != data["Word"][i]):
        tagLemma = ngram.getTagAndLemma(newWord)
        data["Word"][i] = newWord
        data["Tag"][i] = tagLemma[0]
        data["Lemma"][i] = tagLemma[1]
    return data
    
def getEdits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def getEdits2(word):
    return set(e2 for e1 in getEdits1(word) for e2 in getEdits1(e1))

def removeUnknown(words, ngram): 
    return set(w for w in words if ngram.getWordProbability(w)>minKnownWordProb)

def getPossibleWords(word, ngram):
    edit1 = removeUnknown(getEdits1(word), ngram)
    list1 = []
    for i in edit1:
        list1.append([i, edit1Weight])
    df1 = pd.DataFrame(list1, columns = ["Word", "Weight"])
    
    """edit2 = removeUnknown(getEdits2(word), ngram)
    list2 = []
    for i in edit2:
        list2.append([i, edit2Weight])
    df2 = pd.DataFrame(list2, columns = ["Word", "Weight"])
    
    df = pd.concat([df1, df2], ignore_index=True)"""
    df = df1
    return df