import tweepy
import nltk
import pandas as pd
from datetime import datetime
import numpy as np
import operator
from telegram import share_telegram
#Named Entity
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from secrets import consumer_secret, consumer_token, access_token, access_secret

#Sentiment
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#DistilBERT Sentiment
import flair

from SQL_utility import sql



class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.log_path= '/Users/tom/Documents/StockSharks/history.csv'
        self.sid = SentimentIntensityAnalyzer()
        self.DBERT = flair.models.TextClassifier.load('en-sentiment')

    def on_status(self, tweet):

        named_entity = {(' '.join(c[0] for c in chunk), chunk.label() ) for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(tweet.text))) if hasattr(chunk, 'label') and chunk.label()in['ORGANIZATION', 'PERSON']}
        if tweet.retweeted==False and 'RT @' not in tweet.text:# and '@' not in tweet.text:
            df = pd.read_csv(self.log_path, encoding='utf-8')
            source = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            s = flair.data.Sentence(tweet.text)
            self.DBERT.predict(s)
            total_sentiment = s.labels
            orgs = ', '.join([i[0] for i in named_entity])

            df = df.append({'Time': datetime.now(),'Organisations':named_entity, 'Sentiment':total_sentiment[0].value,
                            'Sentiment_Score': total_sentiment[0].score, 'Source':tweet.user.name,'URL':source}, ignore_index=True)
            df = df.set_index(keys='Time', drop=True)
            df.to_csv(self.log_path, encoding='utf-8')
            sql_connection = sql()
            Tickers = sql_connection.identify_live_post_ticker(named_entity)
            if Tickers != [None]:
                new_Tickers = []
                for ind, t in enumerate(Tickers):
                    if t != None and t!= np.nan:
                        new_Tickers.append(t)
                Tickers=new_Tickers
            else:
                Tickers=['']

            if len(Tickers) >1:
                print('Tickers: {}'.format(Tickers))
                ticker_sql = ', '.join([i for i in Tickers])
            else:
                ticker_sql = str(Tickers[0])
            if len(Tickers) >0 and Tickers!=[None]:
                post = 'TIP FROM: {}! \n Mentioned: {} \n Tickers: {} \n Sentiment: {} \n Sentiment Score: {} \n Source: {}'.format(tweet.user.name, orgs, Tickers, total_sentiment[0].value, total_sentiment[0].score, source)
                print('Posted')
                share_telegram(post)

            sql_connection.insert_row(table_name='History',params={'Time': datetime.now(),
                                                                   'Sentiment': total_sentiment[0].value,
                                                                   'Sentiment_Score': round(total_sentiment[0].score,4),
                                                                   'Text':str(tweet.text), 'Organisations': str(orgs),
                                                                   'Source': str(tweet.user.name), 'URL': str(source),
                                                                   'Tickers': ticker_sql})
            print('SQL updated')
        else:
            print('Rejected')
    def on_error(self, status):
        print(status)
        if status == 420:
            #returning False in on_error disconnects the stream
            return False
        print("Error detected")

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print('auth')
StreamListener = MyStreamListener(api)
print('listener')
myStream = tweepy.Stream(auth = api.auth, listener=StreamListener)
print('stream')
following=['185042108', '202915788', "203652149", "2789365139", "22522178",
           "916608044", "959119070959415306", "988955288",
           "1081265101146152961", "1039157087950057473"]
#following=['455639522']#["455639522"] #mine
myStream.filter(follow=following)#, 'KimbleCharting', 'SJosephBurns', 'cryptowat_ch', stocksharks_]) #track=['COVID'])#

print('connected')
