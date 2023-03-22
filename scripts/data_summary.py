# script to quickly assess the dataset

import pandas as pd

PATH_DATA = 'data/final/tweets_66DaysofData.csv'
df = pd.read_csv(PATH_DATA)

# split the `created_at` column into date and time to make aggreation over days possible 
df['created_at'] = pd.to_datetime(df['created_at'])
df['date'] = [d.date() for d in df['created_at']]
df['time'] = [d.time() for d in df['created_at']]

countTweetsDay = df.groupby(['date']).count()['tweet_id']
countTweetsDay = pd.DataFrame(countTweetsDay)
countTweetsDay.rename(columns={'tweet_id': 'count'}, inplace=True)

print("Summary of dataset: ")
print("")
print("tweets: ", df.shape[0])
print("column names: ", list(df.columns.values.tolist()))
print("date range from: ", df['created_at'][0], " to: ", df['created_at'][df. index[-1]])
print("missing values (sould be zero): ", df.duplicated('full_text').sum())
print("Statistics: ")
print("unique participats: ", df['user_id'].nunique())
print("mean: ", countTweetsDay['count'].mean())
print("median: ", countTweetsDay['count'].median())
print("max per day: ", countTweetsDay['count'].max())
print("min per day: ", countTweetsDay['count'].min())




