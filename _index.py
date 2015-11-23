# -*- coding: utf-8 -*-

import pandas as pd
import time

import fixError

start = time.time()

def exists(name):
    return name in locals() or name in globals()

#============================TRAINING DATA=====================================

if(not exists("data_train")):
    allFiles =  ["althingi_tagged\\079.csv",
        "althingi_tagged\\080.csv",
        "althingi_tagged\\081.csv"]
    
    list_ = []
    for file_ in allFiles:
        df_ = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df_)
    data_train = pd.concat(list_)

#==============================TEST DATA=======================================

if(not exists("data_test")):
    data_test = pd.read_csv("althingi_errors\\079.csv", index_col=None, header=0)
    data_test = data_test[0:500]
    data_test = data_test.reset_index(drop=True)

#=============================DICTIONARIES=====================================

if(not exists("d")):
    import dictionaries
    d = dictionaries.d(data_train)

#===============================RESULTS========================================

data_test_result = data_test.copy()
data_test_result["CorrectWord"] = ""

data_test_result = fixError.nonWord(data_test_result, d)
data_test_result = fixError.realWord(data_test_result, d)

#==============================================================================

end = time.time()

def countErrors(c, h):
    cWord = c["CorrectWord"]
    hWord = h["CorrectWord"]
    total = len(hWord)
    count = 0
    
    for i in range(0, total-1):
        word_ = hWord[i]
        if((not pd.isnull(word_)) and word_ != cWord[i]):
            count += 1
    return count/total*100

print("Accuracy: "+str(100-countErrors(data_test, data_test_result))+"%")
print("Time: "+ str(round(end - start)))