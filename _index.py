# -*- coding: utf-8 -*-

import pandas as pd

import ngramResults
import fixError

#to make sure you dont load ngram twice
if(not ("ngram" in locals() or "ngram" in globals())):
    ngram = ngramResults.ngram()

def fixErrors(csv_name):
    data_test = pd.read_csv(csv_name+".csv")
    data_test_result = data_test.copy()
    data_test_result["CorrectWord"] = ""
    
    data_test_result = fixError.nonWord(data_test_result, ngram)
    data_test_result = fixError.realWord(data_test_result, ngram)
    
    data_test_result.to_csv(csv_name+"_result.csv", sep=",", index=False, encoding="utf-8")

# Example:
# fixError(csv_name)
# (creates a csv with the name csv_name+"_result")

#==============================================================================

"""
def printErrorRate(concept, hypothesis):
    cWord = concept["Word"]
    cCWord = concept["CorrectWord"]
    
    hWord = hypothesis["Word"]
    hCWord = hypothesis["CorrectWord"]
    
    total = len(cWord)
        
    countTotal = 0
    countFalsePos = 0
    countFalseNeg = 0
    for i in range(0, total-1):
        if((not pd.isnull(hCWord[i])) and hCWord[i] != cCWord[i]):
            if(cWord[i] == cCWord[i]):
                countFalsePos += 1
            if(hWord[i] == hCWord[i]):
                countFalseNeg += 1
            countTotal += 1
    print("Errors: "+str(countTotal/total*100)+"%"
        +" (false pos: "+str(countFalsePos/total*100)+"%"
        +" false neg: "+str(countFalseNeg/total*100)+"%)")

def printOriginalErrorRate(concept):
    cWord = concept["Word"]
    cCWord = concept["CorrectWord"]
    total = len(cWord)
    
    countOriginal = 0
    for i in range(0, total-1):
        if((not pd.isnull(cWord[i])) and cWord[i] != cCWord[i]):
            countOriginal += 1
    print("Original errors: "+str(countOriginal/total*100)+"%")

csv_name = "080_test"
fixErrors(csv_name)
inputData = pd.read_csv(csv_name+".csv")
outputData = pd.read_csv(csv_name+"_result.csv")
printErrorRate(inputData, outputData)
printOriginalErrorRate(inputData)
"""