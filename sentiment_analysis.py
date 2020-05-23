import re 
import nltk
from nltk import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import pandas as pd
import pickle
# from spellchecker import SpellChecker
# from data_collection import company_dict


_stopwords = set(stopwords.words('english') + ['AT_USER', 'URL', 'rt', '’'])

# spell = SpellChecker()
# add_words = ['tesla', 'microsoft', 'valero', 'tsla', 'msft', 'aapl', 'vlo']
# spell.word_frequency.load_words(add_words)

def processTweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    tweet = re.sub(r'@[^\s]+', 'AT_USER', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = ''.join(ch for ch in tweet if ch not in set(punctuation) - set(['@', '_']))
    tweet = ''.join(ch for ch in tweet if ch not in ['…'])
    tweet = word_tokenize(tweet) 
    return [word for word in tweet if word not in _stopwords]

def getTrainingData(filename):
    df = pd.read_csv(filename)
    trainingData = []
    index = 0
    for tweet in df['TweetText']:
        trainingData.append((processTweet(tweet), df['Sentiment'][index]))
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

trainingData = getTrainingData("full-corpus.csv")
word_features = buildVocabulary(trainingData)
# trainingFeatures = nltk.classify.apply_features(extract_features, trainingData)
# NBayesClassifier=nltk.NaiveBayesClassifier.train(trainingFeatures)
# pickle.dump(NBayesClassifier, open("temp", 'wb'))
classifier = pickle.load(open("corpus_model", 'rb'))
results = [classifier.classify(extract_features(i[0])) for i in trainingData]
print(results)
# print(processTweet("https://www.nasdfas.com www.asfasf.com http://biggasdf.com @person1 RT @person2: Corn hasn't got to be the most delllicious crop in the world!!!! #corn #thoughts..."))
# print(processTweet("RT @Manda_AMSBT: The sole reason why I started drawing when I was 11 was because I wanted to draw inuyasha These don’t do him justice but…"))
# print(processTweet("tesla"))