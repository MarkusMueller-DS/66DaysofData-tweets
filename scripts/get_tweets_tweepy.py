# imports
import os
import tweepy as tw
import pandas as pd
import pickle
import time
from datetime import date
from dotenv import load_dotenv

# load environment variables (keys)
load_dotenv()

# define keys
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET') 
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret =  os.environ.get('ACCESS_TOKEN_SECRET')

# set keys
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# save the date to name the file
date_today = date.today()

# define searchword
# -filter:retweets will exclude the retweets
search_word = '#66daysofdata -filter:retweets' 

# collect tweets
tweets = tw.Cursor(api.search_tweets, q=search_word, lang='en', tweet_mode="extended").items()

# append the tweets in a list
list_tweets = [] # empty list
for tweet in tweets:
    list_tweets.append(tweet)
"""
with open('respnse.txt', 'w') as output:
    output.write(str(list_tweets))
"""

# access the tweets 
# the tweets are in a json for each tweet
# list_tweets[1]._json will give you the json with the information to the first tweet

# create empty lists for each relevant key 
tweet_id = []
user_id = []
user_name = []
created_at = []
text = []
full_text = []
retweets = []
favorite = []

# loop through the list and append the relevant json key to a list
for idx, line in enumerate(list_tweets):
    tweet_id.append(list_tweets[idx]._json['id'])
    user_id.append(list_tweets[idx]._json['user']['id'])
    user_name.append(list_tweets[idx]._json['user']['screen_name'])
    created_at.append(list_tweets[idx]._json['created_at'])
    full_text.append(list_tweets[idx]._json['full_text'])
    retweets.append(list_tweets[idx]._json['retweet_count'])
    favorite.append(list_tweets[idx]._json['favorite_count'])
    
# uses lists to create the pandas DataFrame
d = {'tweet_id': tweet_id, 'user_id': user_id, 'user_name': user_name, 'created_at': created_at, 'full_text': full_text, 
     'retweets': retweets, 'favorite': favorite}
data_df_tweepy = pd.DataFrame(d)

print(f"got {data_df_tweepy.shape[0]} tweets")

# file name
file_name_csv = 'tweets_' + date_today.strftime('%d.%m.%Y') + '_tweepy.csv'
file_name_pkl = 'tweetsData_' + date_today.strftime('%d.%m.%Y') + '_tweepy.pkl'      

# saves the DataFrame as a csv:
data_df_tweepy.to_csv(file_name_csv, index=False)

# saves the original list from tweepy with all the information as a pickl
with open(file_name_pkl, 'wb') as f:
    pickle.dump(list_tweets, f)

PATH_DATA = "data/final/tweets_66DaysofData.csv"
    
# automatically add to csv-db
if os.path.isfile(PATH_DATA):
    print('add new data to csv')
    final_frame = pd.read_csv(PATH_DATA)
    print(f'rows of csv: {final_frame.shape[0]}')
    frames = [data_df_tweepy, final_frame]
    result = pd.concat(frames)

    # make datetime column to sort values by datetime
    result['created_at'] = pd.to_datetime(result['created_at'])

    # sort by date
    result.sort_values(['created_at'], inplace=True)

    # drop for duplicate rows
    results = result.drop_duplicates(subset=['full_text'], keep='last')
    print(f'rows after merging: {results.shape[0]}')
else:
    data_df_tweepy.to_csv(PATH_DATA, index=False)

print('done')
