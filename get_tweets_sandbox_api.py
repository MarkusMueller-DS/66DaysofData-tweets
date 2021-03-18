# imports
import yaml
import searchtweets as st
import json

# load credentials
config = dict(
    search_tweets_api = dict(
        account_type = 'premium',
        # endpoint is specific to you (xxx.json, where xxx is the dev environemtn label)
        endpoint = 'https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json',
        consumer_key = 'XXX', # API key
        consumer_secret = 'XXX' # API secret key
    )
)
with open('cred.yaml', 'w') as config_file:
    yaml.dump(config, config_file, default_flow_style=False)
    
    
# generate bearer token
premium_search_args = st.load_credentials('cred.yaml', yaml_key='search_tweets_api', env_overwrite=False)
# print(premium_search_args)

# define query 
query = '#66daysofdata' 

# define rule (result per call is limited to 100)
rule = st.gen_rule_payload(query, results_per_call=100, from_date='2020-09-01', to_date='2020-10-09 06:00')

# get the tweets (max_result is limited to 5000)
rs = st.ResultStream(rule_payload=rule, max_results=2000, **premium_search_args)

# write to results to a json file
with open('tweetsDatamax.jsonl', 'a', encoding='utf-8') as f:
    for tweet in rs.stream():
        json.dump(tweet, f)
        f.write('\n')
print('done')
