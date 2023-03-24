# script to add new tweets from the Twitter premium-API to the final-frame
import numpy as np
import pandas as pd
from datetime import date, time


file = input('name of csv-file to add: ')

df =pd.read_csv(file)
final_frame = pd.read_csv('finalFrame.csv') 

# replace none in full_text with the input from the text column
df['full_text'] = np.where(df['full_text']=='None', df['text'], df['full_text'])

# delete text column
df.drop('text', 1, inplace=True)

# add new frame to final DataFrame
frames = [df, final_frame]
result = pd.concat(frames)

# make datetime column to sort values by datetime
result['created_at'] = pd.to_datetime(result['created_at'])

# sort by date
result.sort_values(['created_at'], inplace=True)

#print(result['created_at'])
result.to_csv('finalFrame.csv', index=False)

