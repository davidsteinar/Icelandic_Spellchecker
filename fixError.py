# -*- coding: utf-8 -*-

import edits

import pandas as pd
import numpy as np

#==============================================================================

#TODO: change number
minNonWordProbability = 1e-5
minRealWordProbability = 1e-20

def nonWord(data, d):
    for i in range(0, len(data)):
        word_ = data["Word"][i]
        value_ = d.getWordProbability(word_)
        if((not pd.isnull(word_)) and ("." not in word_) and (value_<minNonWordProbability)):
            data["CorrectWord"][i] = getCorrectNonWord(word_, d)
        else:
            data["CorrectWord"][i] = word_    
    
    return data

def getCorrectNonWord(word, d):
    possible = edits.getPossibleWords(word, d)
    possible["Probability"] = 0
    
    for i in range(0, len(possible)):
        weight_ = possible["Weight"][i]
        word_ = possible["Word"][i]
        probability_ = d.getWordProbability(word_)
        possible.loc[i, "Probability"] = weight_*probability_
    
    if(len(possible)>0):
        idMax = possible["Probability"].idxmax()
        return possible["Word"].iloc[idMax]
    else:
        return word

#muna: það má finna edits2 af word ekki correct word
def realWord(data, d):
    data = addNanRows(data)
    Word = list(data["Word"])
    data["value"] = ""
    
    for i in range(1, len(data)-1):
        word_ = Word[i]
        data_ = data[i-1:i+2]
        value_ = d.getValue(data_)
        if(not pd.isnull(word_) and value_<minRealWordProbability):
            data["CorrectWord"][i] = getCorrectRealWord(data_, d)
            data["value"][i] = value_
        else:
            data["CorrectWord"][i] = data["Word"][i]    
    
    #removing the top and bottom NaN row we added earlier
    data = data[1:len(data)-1]
    return data.reset_index(drop=True)

def addNanRows(data):
    newData = pd.DataFrame(columns=data.columns)
    newData.loc[0] = np.nan
    newData = newData.append(data, ignore_index=True)
    newData.loc[len(newData)] = np.nan
    return newData

def getCorrectRealWord(data, d):
    data = data.reset_index(drop=True)
    word = data["Word"][1]

    #adding the current word to the top of the list in case all possibilities
    #are equally probable
    df1 = pd.DataFrame([[word, edits.edit1Weight]], columns=["Word", "Weight"]) 
    df2 =  edits.getPossibleWords(word, d)
    possible = pd.concat([df1, df2], ignore_index=True)
    possible["Probability"] = 0
    
    data = updateTrigramLemmaAndTag(data, data["CorrectWord"][0], 0, d)
    data = updateTrigramLemmaAndTag(data, data["CorrectWord"][2], 2, d)
    
    for i in range(0, len(possible)):
        weight_ = possible["Weight"][i]
        data_ = updateTrigramLemmaAndTag(data, possible["Word"][i], 1, d)        
        probability_ = d.getValue(data_)
        possible.loc[i, "Probability"] = weight_*probability_
    
    if(len(possible)>0):
        idMax = possible["Probability"].idxmax()
        return possible["Word"].iloc[idMax]
    else:
        return word

def updateTrigramLemmaAndTag(data, newWord, i, d):
    if(not pd.isnull(newWord) and newWord != data["Word"][i]):
        tagLemma = d.getTagAndLemma(newWord)
        data["Word"][i] = newWord
        data["Tag"][i] = tagLemma[0]
        data["Lemma"][i] = tagLemma[1]
    return data
