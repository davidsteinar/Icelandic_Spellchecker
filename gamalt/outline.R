#gets all the csv's in althingi_tagged [dataframe: word,tag,lemma]
data_train = getTrainData()

#get all the csv's in althingi_error, and removes the correctWord col [dataframe: word,tag,lemma]
data_test = getTestData() 

#counts each word [dataframe: word, tag, lemma, freq]
dictionary = getDictionary(data_train)

#fixes all non-word error [data.frame: word,tag,lemma,correctWord]
data_test = fixNonWordErrors(dictionary, data_test)
fixNonWordErrors = function(dictionary, data) {
  data$correctWord = data$word
  
  for(i in (1:nrow(data))) {
    freq = dictionary$freq[dictionary$word==data$word[i]]
    if(freq < 1) {
      #takes in a word, finds possible candidates, and chooses the one with the highest
      #frequency in dictionary [word]
      data$correctWord[i] = getCorrectWord(dictionary, data$word[i])
    }
  }
  
  return(data)
}

#fixes all real-word error (changes the correctWord column) [data.frame: word,tag,lemma,correctWord]
data_test = fixRealWordErrors(dictionary, data_test)
fixRealWordErrors = function(dictionary, data) {
  #counts all bigrams [sparse matrice?]
  bigramDictionary = getBigramDictionary(dictionary)
  
  #counts all trigrams [3D sparse matrice?]
  trigramDictionary = getTrigramDictionary(dictionary)
  
  for(i in (1:nrow(data)-2)) {
    trigram = c(data$correctWord[i], data$correctWord[i+1], data$correctWord[i+2])
    
    #calculates the odds of the middle word being there (sum of bi- and trigram freq?)
    odds = getTrigramOdds(bigramDictionary, trigramDictionary, trigram)
    
    if(odds<0.1) {
      #finds the correct word by finding all candidates for the middle word in trigram
      #and choosing the one with the highest trigramOdds
      data$correctWord[i] = getCorrectWord(bigramDictionary, trigramDictionary, trigram)
    }
    
  }
  
  return(data)
}
