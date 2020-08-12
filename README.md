# Stocks Predictor 
This is an experimental project which unfortunately was not able to come up with a good stock prediction algorithm. However, it did lead to a lot of interesting data collection, and sentiment analysis research.

## Project Structure
`data_collection.py`: loops through all companies specified in a dictionary with all their "search terms". Collects relevant tweets using the Twitter API, and downloads their test, along with other relevant information (retweets, likes, etc.) into a csv file.  
`clean_data.py`: Goes through the collected raw data, runs sentiment analysis on all the tweets and consolidates each companies data by date along with their stock's performance for the next 5 days through yfinance. It then saves this "cleaned data" to a csv file.  
`stock_prediction.py`: Takes all the clean data and runs a series of algorithms to try and fit the data. It turns out that the next days stock value change is usually the best prediction, and that simpler models (linear, degree 1 or 2) tend to perform the best as to not over fit the training data. Still, no breakthrough results occurred.  
`sentiment_analysis.py`: This file was used to test various methods of training a sentiment analysis algorithm. Naive Bayes was used on multiple datasets of various sizes, some hand labeled. This file also tested out using the stanford corpus as well as the stanford made algorithm which runs in java. In the end, for the actual stock prediction, the vader library was used for its speed as well as its decent accuracy.  
`collect_and_clean.sh`: script that runs data collection automatically on my machine using anacron.  
`stanford_dataset_model`: directory which stores sentiment analysis model for stanford dataset.  
`twitter_corpus_model`: directory which stores sentiment analysis model for twitter corpus dataset which was found online.

## Steps for reproduction
I have kept my private keys needed to use the twitter API in a file called private-keys. If one wanted to use the same data collection they would need to set up their access to the twitter API and do the same. 

If one wishes to have the automatic collection of data they should also setup up cron/anacron on their machine and use the `collect_and_clean` script.

Other than that, the two sentiment analysis models are ready to use, with accuracy of around 60%. The stock prediction so far has only been succesful on relatively stable companies, and has a high RMSE on companies that fluctuate wildly. This suggests that the twitter data received is not a good measure on the companies future stock price.
