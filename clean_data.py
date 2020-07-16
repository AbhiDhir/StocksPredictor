from nltk.sentiment.vader import SentimentIntensityAnalyzer
import operator
import pandas as pd
import yfinance as yf

vader = SentimentIntensityAnalyzer()
twitter_data_csv = "raw-twitter-data.csv"
cleaned_data = "clean-twitter-data.csv"
stock_to_ticker_dict = {"tesla": "TSLA", "microsoft": "MSFT", "apple": "AAPL", "valero": "VLO"}

raw_twitter_data = pd.read_csv(twitter_data_csv)
clean_twitter_data = []

# # Only needs to run once, sets up headers
# data = {}
# df = pd.DataFrame(data, columns= ['company', 'date', 'numNegative', 'numNeutral', 
#                                   'numPositive', 'confNegative', 'confNeutral', 'confPositive',
#                                   'negFollowers', 'neuFollowers', 'posFollowers',
#                                   'negLikes', 'neuLikes', 'posLikes',
#                                   'negRetweets', 'neuRetweets', 'posRetweets',
#                                   'oneDayChange', 'twoDayChange', 'threeDayChange', 'fiveDayChange'])
# df.to_csv(cleaned_data, mode='w', index = False, header=True)
# with open(cleaned_data, 'a') as f:
#     f.write('\n')

def populate_fields(current_entry, predicted_sentiment, polarity_score):
    if(predicted_sentiment == 'neg'):
        current_entry['numNegative'] += 1
        current_entry['confNegative'] += (polarity_score[predicted_sentiment] - current_entry['confNegative']) / current_entry['numNegative']
        current_entry['negFollowers'] += row['followers']
        current_entry['negLikes'] += row['likes']
        current_entry['negRetweets'] += row['retweets']
    elif(predicted_sentiment == 'neu'):
        current_entry['numNeutral'] += 1
        current_entry['confNeutral'] += (polarity_score[predicted_sentiment] - current_entry['confNeutral']) / current_entry['numNeutral']
        current_entry['neuFollowers'] += row['followers']
        current_entry['neuLikes'] += row['likes']
        current_entry['neuRetweets'] += row['retweets']
    else:
        current_entry['numPositive'] += 1
        current_entry['confPositive'] += (polarity_score[predicted_sentiment] - current_entry['confPositive']) / current_entry['numPositive']
        current_entry['posFollowers'] += row['followers']
        current_entry['posLikes'] += row['likes']
        current_entry['posRetweets'] += row['retweets']

    return current_entry

def initializeEntry(row):
    current_entry = {}

    current_entry['company'] = row['company']
    current_entry['date'] = row['date']
    current_entry['numNegative'] = 0
    current_entry['numNeutral'] = 0
    current_entry['numPositive'] = 0
    current_entry['confNegative'] = 0
    current_entry['confNeutral'] = 0
    current_entry['confPositive'] = 0
    current_entry['negFollowers'] = 0
    current_entry['neuFollowers'] = 0
    current_entry['posFollowers'] = 0
    current_entry['negLikes'] = 0
    current_entry['neuLikes'] = 0
    current_entry['posLikes'] = 0
    current_entry['negRetweets'] = 0
    current_entry['neuRetweets'] = 0
    current_entry['posRetweets'] = 0

    return current_entry

current_entry = initializeEntry({'company': 'test', 'date': 'test'})

for index, row in raw_twitter_data.iterrows():
    polarity_score = vader.polarity_scores(row['text'])
    del polarity_score['compound']
    predicted_sentiment = max(polarity_score.items(), key=operator.itemgetter(1))[0]

    if(current_entry['company'] != row['company'] or current_entry['date'] != row['date']):
        if(current_entry['company'] != 'test'):
            date = current_entry['date']
            company = yf.Ticker(stock_to_ticker_dict[current_entry['company']])
            history = company.history(start=date)
            
            startPrice = history['Open'][0]
            oneDay = history['Close'][0] - startPrice
            twoDay = history['Close'][1] - startPrice
            threeDay = history['Close'][2] - startPrice
            fiveDay = history['Close'][4] - startPrice

            current_entry['oneDayChange'] = oneDay
            current_entry['twoDayChange'] = twoDay
            current_entry['threeDayChange'] = threeDay
            current_entry['fiveDayChange'] = fiveDay

            clean_twitter_data.append(current_entry)

        current_entry = initializeEntry(row)

    current_entry = populate_fields(current_entry, predicted_sentiment, polarity_score)

df = pd.DataFrame(clean_twitter_data) 
df.to_csv(cleaned_data, mode='a', index=False,header=False)

rawData = raw_twitter_data[0:0]
rawData.to_csv(twitter_data_csv, mode='w', index=False, header=True)