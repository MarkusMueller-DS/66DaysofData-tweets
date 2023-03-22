import pandas as pd
import unittest

class TestData(unittest.TestCase):

    PATH_DATA = 'data/final/tweets_66DaysofData.csv'
    df = pd.read_csv(PATH_DATA)

    def test_cols(self):
        col_names = ['tweet_id', 'user_id', 'user_name', 'created_at', 'full_text', 'retweets', 'favorite', 'date', 'time']
        self.assertEqual(list(df.columns.tolist())[0], col_names[0])

    def test_date(self):
        date = "2020-08-29 06:55:13+00:00"
        self.assertEqual(df.iloc[0]["created_at"], date)

if __name__ == '__main__':
    PATH_DATA = 'data/final/tweets_66DaysofData.csv'
    df = pd.read_csv(PATH_DATA)

    print("Quality of dataset: ")
    print("tweets: ", df.shape[0])
    print("date range from: ", df['created_at'][0], " to: ", df['created_at'][df. index[-1]])
    print("missing values (sould be zero): ", df.duplicated('full_text').sum())
    print("unique participats: ", df['user_id'].nunique())

    unittest.main()

