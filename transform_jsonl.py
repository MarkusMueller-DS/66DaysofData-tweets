# this script transforms the result json-file from the twitter-premium-API 
# to a usable csv-file

import pandas as pd
import json

# user can inpur filname
file = input('name of json-file: ')

# read json
tweets = []
for line in open(file, 'r'):
    tweets.append(json.loads(line))
    

## filter rewteets
# list to append the idx of tweets with 'RT' in text
idx_retweets = []
for idx, line in enumerate(tweets):
    s = tweets[idx]['text']
    if 'RT' in s:
        idx_retweets.append(idx)
        
# list comprehensions to exclude tweets that are in idx_retweets
unique_tweets = [i for j, i in enumerate(tweets) if j not in idx_retweets]

# define important columns
tweet_id = []
user_id = []
user_name = []
created_at = []
text = []
full_text = []
retweets = []
favorite = []

# go through unique_teets and append input to the coressponding list 
for idx, line in enumerate(unique_tweets):
    tweet_id.append(unique_tweets[idx]['id'])
    user_id.append(unique_tweets[idx]['user']['id'])
    user_name.append(unique_tweets[idx]['user']['screen_name'])
    created_at.append(unique_tweets[idx]['created_at'])
    text.append(unique_tweets[idx]['text'])
    try:
        full_text.append(unique_tweets[idx]['extended_tweet']['full_text'])
    except:
        full_text.append('None')
    retweets.append(unique_tweets[idx]['retweet_count'])
    favorite.append(unique_tweets[idx]['favorite_count'])
    
# create DataFrame
d = {'tweet_id': tweet_id, 'user_id': user_id, 'user_name': user_name, 'created_at': created_at, 'text': text, 'full_text': full_text, 'retweets': retweets, 'favorite': favorite}
data_df = pd.DataFrame(d)

# spilt file to only get the name
filename = file.split('.')[0] + '.csv'

# save DataFrame as csv
data_df.to_csv(filename, index=False)
