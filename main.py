from monkeylearn import MonkeyLearn 
import yfinance as yf
import twitter
import pickle

## API KEYS ##
filepath_to_keys = "private-keys" # Hidden file containing private keys
key_dict = pickle.load(open(filepath_to_keys, 'rb'))

ml_model_id = 'cl_qkjxv9Ly' # Sentiment Analysis specialized for tweets
ml_private_key = key_dict['ml_private_key']

twitter_consumer_key = key_dict['twitter_consumer_key']
twitter_consumer_secret_key = key_dict['twitter_consumer_secret_key']
twitter_access_token_key = key_dict['twitter_access_token_key']
twitter_access_token_secret = key_dict['twitter_access_token_secret']

## API Models ##
ml = MonkeyLearn(ml_private_key)
twtr = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret_key,
                  access_token_key=twitter_access_token_key,
                  access_token_secret=twitter_access_token_secret)

## Testing ## 
results = twtr.GetSearch(
    raw_query="q=tesla%20&result_type=recent&since=2014-07-19&count=10"
)
print(results)
data = [results[0].text.strip()]
# data = ["it’s safe to say that @elonmusk and @TeslaMotors’ ambition to accelerate the advent of sustainable transport is a #success :-)"]
result = ml.classifiers.classify(ml_model_id, data)
print(result.body)