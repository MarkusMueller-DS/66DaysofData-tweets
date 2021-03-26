# 66DaysofData tweets Analysis (WIP)
Analysis of tweets from the #66DaysofData community/challenge

### Challenges
- Get historical tweets isn't easy. 
- Twitter-premium API has a limit query amount per month
- Oher Twitter APIs can only retrieve tweets with full-text up to one week

### Files
- Data_Warangling.ipynb: Jupyter Notebook with the process of creating the final Dataframe
- Hashtag_analysis.ipynb: Jupyter Notebook with the analysis of the tweets
- get_tweets_sandbox_api.py: Python script to access the Twitter API and get historical tweet data
- get_tweets_tweepy.py: Python script to access tweets up to one week
- transform_json.py: Python script to transforme the result of the Twitter premium API to a usable csv-file
- append_p_premium.py: Python script to append the result of (transform_json.py) to the final Dataframe


### ToDO
- complete data gathering (use Twitter API to get historical data before 03.10.2020)
- make a more simpler data gathering pipeline. At this point I have to do various steps in differrent environments to have a final DataFrame with all the data

### First results
- How many total tweets?
    - 14181
- How many unique participants?
    - 779
- Basic statistics on tweets?
    - mean: 67.8
    - median: 69.0
    - max: 165
    - min: 8
- Day with most tweets / Day with least tweets
    - min tweets: 8 tweets on 19th and 20th of Decemer 2020
    - max tweets: 2nd of September 2020, (one day after the start)
- Who was the most active user?
    - paulapivat (173 tweets)
