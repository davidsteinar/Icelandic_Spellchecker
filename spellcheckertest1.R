temp = list.files(path="althingi_tagged/",pattern="*.csv")
#for (i in 1:length(temp)) assign(temp[i], read.csv(paste("althingi_tagged/",temp[i],sep="/"), encoding = 'UTF-8'))
althingi <- read.csv("althingi_tagged/079.csv", encoding = 'UTF-8' )

word_count <- table(althingi$Word)
sorted_words <- names(sort(word_count, decreasing = TRUE))

lemma_count <- table(althingi$Lemma)
sorted_lemmas <- names(sort(lemma_count, decreasing = TRUE))

tag_count <- table(althingi$Tag)
sorted_tags <- names(sort(tag_count, decreasing = TRUE))

correct <- function(word) {
  # Calculate the edit distance between the word and all other words in sorted_words.
  edit_dist <- adist(word, sorted_words)
  # Calculate the minimum edit distance to find a word that exists in big.txt 
  # with a limit of two edits.
  min_edit_dist <- min(edit_dist, 2)
  # Generate a vector with all words with this minimum edit distance.
  # Since sorted_words is ordered from most common to least common, the resulting
  # vector will have the most common / probable match first.
  proposals_by_prob <- c(sorted_words[ edit_dist <= min(edit_dist, 2)])
  # In case proposals_by_prob would be empty we append the word to be corrected...
  proposals_by_prob <- c(proposals_by_prob, word)
  # ... and return the first / most probable word in the vector.
  proposals_by_prob[1]
}

#In : takes in a dataframe column containing lemmas
#Out: returns a bigram dictionary with counts
bigramdict <- function(lemma){
  #preallocate bigram vector
  bi <- matrix(0,length(lemma)-1,1) 
  for (i in 1:length(bi)){
    bi[i] <- paste(lemma[i],lemma[i+1])
  }
  return(table(bi))
  
}

#takes in a column of taggs and returns a trigram dictionary with counts
trigramdict <- function(tagg){
  #preallocate trigram vector
  tri <- matrix(0,length(tagg)-2,1)
  for (i in 1:length(tri)){
    tri[i] <- paste(tagg[i],tagg[i+1],tagg[i+2])
  }
  return(table(tri))
}

bigrams <- bigramdict(althingi$Lemma)
trigrams <- trigramdict(althingi$Tag)

#write.csv(bigrams,'bigrams.csv',row.names = FALSE) #to save the results

