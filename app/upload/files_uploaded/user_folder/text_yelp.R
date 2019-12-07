##############################################################
# Basics of Text Mining, D3M NYU Stern
# Exercises from Karsten Hansen, UCSD
##############################################################

# 1) Basics of Yelp review
# 2) Word frequency and word cloud
# 3) Topic models & sentiment 
rm(list=ls())
install.packages("dplyr")
install.packages("tidyr")
install.packages("slam")
install.packages("topicmodels")
install.packages("wordcloud")
install.packages("ggmap")
install.packages("SnowballC")
install.packages("tm")

#setwd("X:/Dropbox/19-NYU/Teaching/D3M/Xiao/Spring17/GB-M/Lectures/L22 C3-Yelp2")
setwd("/Users/xiaoliu/Dropbox/19-NYU/Teaching/D3M/Xiao/Spring17/GB-M/Lectures/L22 C3-Yelp2")


library(dplyr)
library(ggplot2)
library(tidyr)
library(ggmap)
library(cluster)   
library(tm)
library(topicmodels)
library(slam)
library(SnowballC)

#load.yelp data

load('vegas_hotels.rda')

# summarize.reviews
reviews %>%
  left_join(select(business,business_id,name),
            by='business_id') %>%
  group_by(name) %>%
  summarize(n = n(), #n() is the count of observations
            mean.star = mean(as.numeric(stars))) %>%
  arrange(desc(mean.star)) %>%
  ggplot() + 
  geom_point(aes(x=reorder(name,mean.star),y=mean.star,size=n))+
  coord_flip() +
  ylab('Mean Star Rating (1-5)') + 
  xlab('Hotel')

##########################################################################################
# ANALYZE TeXT OF REVIEWS
# SUBSET TO 1 Hotel for simplicity
#########################################################################################

## extract reviews for 1 hotel: Aria.reviews

aria.id <-  filter(business, 
                   name=='Aria Hotel & Casino')$business_id
aria.reviews <- reviews %>% filter(business_id==aria.id) %>% mutate(doc_id=review_id)

#########################################################################################
## clean.aria.reviews & Create DTM

# Corpus is a collection of text documents
# DTM: frequency of terms that occur in a collection of documents

# Read intro to TM Package https://cran.r-project.org/web/packages/tm/vignettes/tm.pdf
########################################################################################
review.corpus <- VCorpus(DataframeSource(aria.reviews)) #Create volatile corpora
#transaformation of the corpora
#review.corpus.clean <- tm_map(review.corpus, content_transformer(tolower)) #Interface to apply transformation functions to corpora.
#if the line above does not work and you use a MAC, try this
review.corpus.clean <- tm_map(review.corpus, content_transformer(function(x) iconv(x, to='UTF-8-MAC', sub='byte')))
review.corpus.clean <- tm_map(review.corpus.clean, content_transformer(tolower)) #Interface to apply transformation functions to corpora.
review.corpus.clean <- tm_map(review.corpus.clean, removeWords, stopwords("english"))
review.corpus.clean <- tm_map(review.corpus.clean, removePunctuation)
review.corpus.clean <- tm_map(review.corpus.clean, removeNumbers)
review.corpus.clean <- tm_map(review.corpus.clean, stemDocument, language="english") #perform stemming which truncates words
review.corpus.clean <- tm_map(review.corpus.clean,stripWhitespace)

dtm <- DocumentTermMatrix(review.corpus.clean)
inspect(dtm[1:10,c("new","room")])

## Check frequency and make frequency plot
freq <- colSums(as.matrix(dtm))
freq[1:10]

#Very hard to see, so let's make a plot
term.count <- as.data.frame(as.table(dtm)) %>%
  group_by(Terms) %>%
  summarize(n=sum(Freq))

# Keep High Frequency words only
term.count %>% 
  filter(cume_dist(n) > 0.9975) %>% #cume_dist is the cumulative distribution function which gives the proportion of values less than or equal to the current rank
  ggplot(aes(x=reorder(Terms,n),y=n)) + geom_bar(stat='identity') + 
  coord_flip() + xlab('Counts') + ylab('')

#Another way to find the frequent terms 
findFreqTerms(dtm, lowfreq=150)


 # find terms correlated with "room" 
room <- data.frame(findAssocs(dtm, "room", 0.35))
room %>%
  add_rownames() %>%
  ggplot(aes(x=reorder(rowname,room),y=room)) + geom_point(size=4) + 
  coord_flip() + ylab('Correlation') + xlab('Term') + 
  ggtitle('Terms correlated with Room') + theme(text=element_text(size=20))

bathroom <- data.frame(findAssocs(dtm, "bathroom", 0.2))

bathroom %>%
  add_rownames() %>%
  ggplot(aes(x=reorder(rowname,bathroom),y=bathroom)) + geom_point(size=4) + 
  coord_flip() + ylab('Correlation') + xlab('Term') + 
  ggtitle('Terms correlated with Bathroom')


## Make wordcloud
#install.packages("wordcloud")
library(wordcloud)
popular.terms <- filter(term.count,n > 200)
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"))

###########################################################################################
# SENTIMENT ANALYSIS
# R package: Download the packages to your computer from the links
###########################################################################################
install.packages("SentimentAnalysis")
library(SentimentAnalysis)
sentiment <- analyzeSentiment(aria.reviews$text)

#if the above line does not work and you have a MAC, try this
recode <-function(x) {iconv(x, to='UTF-8-MAC', sub='byte')}
sentiment <- analyzeSentiment(recode(aria.reviews$text))

sent_df = data.frame(polarity=sentiment$SentimentQDAP, business = aria.reviews, stringsAsFactors=FALSE)

# Plot results and check the correlation betweeen polarity and review stars
sent_df$business.stars<-as.numeric(sent_df$business.stars)
sent_df %>%
  group_by(business.stars) %>%
  summarize(mean.polarity=mean(polarity,na.rm=TRUE)) %>%
  ggplot(aes(x=business.stars,y=mean.polarity)) +  geom_bar(stat='identity',fill="blue") +  
  ylab('Mean Polarity') + xlab('Stars')  + theme(text=element_text(size=20))


# Create helpful variable and plot by helpful
sent_df$helpful[sent_df$business.votes.useful==0]<-"Not Helpful"
sent_df$helpful[sent_df$business.votes.useful!=0]<-"Helpful"

spineplot(as.factor(sent_df$helpful)~as.factor(sent_df$business.stars),col = c("red3", "grey", "green3"))
#Correlation between helpfulness and polarity
summary(sent_df)
#correct for NA
sent_df$polarity[is.na(sent_df$polarity)]=0
#change useful from factor to numeric
sent_df$business.votes.useful=as.numeric(paste(sent_df$business.votes.useful))
#correlation between polarity and useful
cor(sent_df$polarity,sent_df$business.votes.useful)

###########################################################################################
# TOPIC MODELING
# R package: "topicmodels"
###########################################################################################

## set.up.dtm.for.lda.1
library(topicmodels)
library(slam)

dtm.lda <- removeSparseTerms(dtm, 0.98)
review.id <- aria.reviews$review_id[row_sums(dtm.lda) > 0]
dtm.lda <- dtm.lda[row_sums(dtm.lda) > 0,]

## run LDA algorithm - WARNING: takes a while to run!
lda.aria <- LDA(dtm.lda,k=20,method="Gibbs",
                control = list(seed = 2011, burnin = 1000,
                               thin = 100, iter = 5000))
save(lda.aria,file='lda_results.rda')

## load results (so you don't have to run the algorithm)

load('lda_results.rda')

post.lda.aria <- posterior(lda.aria) #get the posterior probability of the topics for each document and of the terms for each topic


##  sum.lda
sum.terms <- as.data.frame(post.lda.aria$terms) %>% #matrix topic * terms
  mutate(topic=1:20) %>% #add a column
  gather(term,p,-topic) %>% #gather makes wide table longer, key=term, value=p, columns=-topic (exclude the topic column)
  group_by(topic) %>%
  mutate(rnk=dense_rank(-p)) %>% #add a column
  filter(rnk <= 10) %>%
  arrange(topic,desc(p)) 


sum.terms %>%
  filter(topic==1) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 1') + theme(text=element_text(size=20))

sum.terms %>%
  filter(topic==2) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 2') + theme(text=element_text(size=20))

sum.terms %>%
  filter(topic==3) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 3') + theme(text=element_text(size=20))

sum.terms %>%
  filter(topic==8) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 8')

sum.terms %>%
  filter(topic==10) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 10')


sum.terms %>%
  filter(topic==12) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 12')

sum.terms %>%
  filter(topic==18) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 18')

sum.terms %>%
  filter(topic==19) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 19')

## @knitr sum.topics  
topics.df <- as.data.frame(post.lda.aria$topics) %>% #this can be used as features
  mutate(doc=1:2009) %>%
  gather(topic,p,-doc) %>%
  arrange(doc,desc(p))

doc.top.topic <- topics.df %>% 
  group_by(doc) %>%
  mutate(rnk=dense_rank(-p)) %>%
  filter(rnk <= 3) %>%
  arrange(doc)

##  mean.ratings.by.topic
review.id.df <- data.frame(doc=1:2009,review_id=review.id) %>%
  left_join(select(aria.reviews,review_id,stars),by='review_id')

topics.df %>%
  group_by(doc) %>%
  filter(p > .08) %>%
  arrange(doc) %>%
  left_join(review.id.df,by='doc') %>%
  group_by(topic) %>%
  summarize(mean.stars=mean(as.numeric(stars))) %>%
  ggplot(aes(x=reorder(topic,mean.stars),y=mean.stars)) + geom_point(size=4) +  
  ylab('Mean Rating') + xlab('Documents containing Topic') + coord_flip() 

aria.review.subset <- aria.reviews[aria.reviews$review_id %in% review.id,]
topic.df <-post.lda.aria$topics
combined.df <- data.frame(aria.review.subset,topic.df)

maxtopic <- max.col(topic.df)
review.topic.df <- data.frame(review_id=review.id,Topic=maxtopic) %>%
  left_join(aria.reviews,by='review_id')
