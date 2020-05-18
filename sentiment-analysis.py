import re 
from nltk.word_tokenize import word_tokenize
from string import punctuantion
from nltk.corpus import stopwords

_stopwords = set(stopwords.words('english') + list(punctuantion))

def processTweet(tweet):
    tweet = tweet.lower() # convert text to lower-case
    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
    tweet = re.sub(r'@[^\s]+', 'AT_USER', tweet) # remove usernames
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
    tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
    return [word for word in tweet if word not in _stopwords]