import re 
import nltk
from nltk import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import pandas as pd
import pickle
import demoji

_stopwords = set(stopwords.words('english') + ['rt', '’'])

def processTweet(tweet):
    tweet = demoji.replace(tweet) #removes emoticons
    tweet = tweet.lower() #lowercase
    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', '', tweet) #removes urls
    tweet = re.sub(r'@[^\s]+', '', tweet) #removes usernames
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #removes hastags
    tweet = ''.join(ch for ch in tweet if ch not in set(punctuation)) # removes punctuation
    tweet = ''.join(ch for ch in tweet if ch not in ['…']) #removes elipses (not included in punctuation)
    tweet = word_tokenize(tweet) # tokenize string into list
    return [word for word in tweet if word not in _stopwords] # removes english stopwords

def minimumProcessTweet(tweet):
    return [e.lower() for e in tweet.split() if len(e) >= 3]

def getTrainingData(filename, cols):
    df = pd.read_csv(filename, header=None, names=cols, encoding="ISO-8859-1")
    trainingData = []
    index = 0
    for tweet in df['text']:
        # trainingData.append((minimumProcessTweet(tweet), df['sentiment'][index]))
        trainingData.append((processTweet(tweet), df['sentiment'][index]))
        index+=1
    return trainingData

def buildVocabulary(trainingData):
    all_words = []
    
    for (words, sentiment) in trainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()
    
    return word_features

def extract_features(tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features['contains(%s)' % word]=(word in tweet_words)
    return features 

### Stanford Dataset Model (~1,600,000 tweets, higher accuracy) ###
# cols = ['sentiment', 'id', 'date', 'query_string', 'user', 'text']
# trainingData = getTrainingData("./stanford_dataset_model/trainingandtestdata/training.1600000.processed.noemoticon.csv", cols)
# pickle.dump(trainingData, open("stanford_dataset_model/trainingData", "wb"))
# pickle.dump(trainingData, open("stanford_dataset_model/minimumProcessedTrainingData", "wb"))
# trainingData = pickle.load(open("stanford_dataset_model/trainingData", "rb"))
# word_features = buildVocabulary(trainingData)
# trainingFeatures = nltk.classify.apply_features(extract_features, trainingData)

# classifier = nltk.NaiveBayesClassifier.train(trainingFeatures)
# pickle.dump(classifier, open("stanford_dataset_model/model", "wb"))
# classifier = pickle.load(open("stanford_dataset_model/model", "rb"))

### Twitter Corpus Model (~3500 tweets, low accuracy) ###
# trainingData = getTrainingData("./twitter_corpus_model/full-corpus.csv", None)
# word_features = buildVocabulary(trainingData)
# trainingFeatures = nltk.classify.apply_features(extract_features, trainingData)
# NBayesClassifier=nltk.NaiveBayesClassifier.train(trainingFeatures)
# pickle.dump(NBayesClassifier, open("corpus_model", 'wb'))
# classifier = pickle.load(open("corpus_model", 'rb'))