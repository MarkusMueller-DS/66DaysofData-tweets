import pandas as pd

df = pd.read_csv('finalFrame.csv')

df = df.drop_duplicates(subset=['full_text'], keep='last')

df.to_csv('finalFrame.csv', index=False)

if df.duplicated('full_text').sum() == 0: 
    print("duplicates haven been removed")
else:
    print("somthing went wrong")
