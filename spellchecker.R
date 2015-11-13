library(data.table)
#----------#make a total word dictionary with wordcount
dictionary <- c()
speech <- read.csv('079.csv', dec=",", encoding = "UTF-8")
speech <- data.table(speech)
dictionary <- c(speech$Word)
tagg <- c(speech$Tag)
merge <- c(tagg, dictionary)
dictable <- data.table(merge)


#----------#Make a bigram dictionary out of Lemmas

#----------#Make a trigram dictionary out of the Tags 

#----------#make a 1 edit distance wordscrambler

#----------#correct all non-word errors in sentence

#----------#Go over sentence again with n-grams method


