from datetime import date, timedelta
import twitter
import pickle
import pandas as pd

## Files ##
filepath_to_keys = "private-keys" # Hidden file containing private keys
twitter_data_csv = "raw-twitter-data.csv"

## Companies ##
""" Format: [Stock, Company Name, CEO] spaces replaced by '+' """
company_dict = {"tesla" : ["tsla", "tesla", "elon+musk"],
                "microsoft": ["msft", "microsoft", "satya+nadella"],
                "apple": ["aapl", "apple", "tim+cook"],
                "valero": ["vlo", "valero", "joseph+w.+gorder"]}

## API KEYS ##
key_dict = pickle.load(open(filepath_to_keys, 'rb'))

ml_model_id = 'cl_qkjxv9Ly' # Sentiment Analysis specialized for tweets
ml_private_key = key_dict['ml_private_key']

twitter_consumer_key = key_dict['twitter_consumer_key']
twitter_consumer_secret_key = key_dict['twitter_consumer_secret_key']
twitter_access_token_key = key_dict['twitter_access_token_key']
twitter_access_token_secret = key_dict['twitter_access_token_secret']

## API Models ##
# ml = MonkeyLearn(ml_private_key)
twtr = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret_key,
                  access_token_key=twitter_access_token_key,
                  access_token_secret=twitter_access_token_secret)

## Data Collection ## 
# Only needs to run once, sets up headers
# df = pd.DataFrame(data, columns= ['id', 'company', 'date', 'text', 'followers', 
                                #   'likes', 'retweets'])
# df.to_csv('raw-twitter-data.csv', mode='w', index = False, header=True)
# with open(twitter_data_csv, 'a') as f:
    # f.write('\n')

today = date.today()

# generate queries
query_dict = {}
for company in company_dict.keys():
    query_dict[company] = []
    for search_term in company_dict[company]:
        query_dict[company].append("q=%s&result_type=mixed&since=%s&until=%s&count=100&lang=en" % 
                            (search_term, str(today-timedelta(days=7)), str(today-timedelta(days=6))))

# request twitter api
raw_twitter_data = {}
for company in query_dict.keys():
    for query in query_dict[company]:
        twitter_result = twtr.GetSearch(
            raw_query=query
        )
        for tweet in twitter_result:
            # check for duplicate tweets
            if(tweet.id not in raw_twitter_data):
                raw_twitter_data[tweet.id] = [company, str(today-timedelta(days=7)), 
                                            tweet.text, tweet.user.followers_count, 
                                            tweet.favorite_count, tweet.retweet_count]

# get data in correct format                                      
twitter_data = [] 
for tweet_id, tweet_data in raw_twitter_data.items():
    tweet = [tweet_id] + tweet_data
    twitter_data.append(tweet)

# write to file
df = pd.DataFrame(twitter_data) 
df.to_csv(twitter_data_csv, mode='a', index=False,header=False)