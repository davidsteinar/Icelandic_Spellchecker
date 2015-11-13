#temp = list.files(path="althingi_tagged/",pattern="*.csv")
#for (i in 1:length(temp)) assign(temp[i], read.csv(paste("althingi_tagged/",temp[i],sep="/")))
althingi <- read.csv("althingi_tagged/079.csv")

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