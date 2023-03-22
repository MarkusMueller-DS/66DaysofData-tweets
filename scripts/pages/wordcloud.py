import numpy as np
import pandas as pd
import streamlit as st
import re
import random
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud


def create_random_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to create a DataFrame with tweets from a random participant
    df: main DataFrame with every tweet
    """
    print("create wordcloud for random user")
    # find random user 
    unique_user = df['user_id'].unique()
    random_user_id = random.choice(unique_user)
    user_name = df[df['user_id'] == random_user_id]['user_name'].values[0]

    df = df[df['user_name']==user_name]
    df = df.reset_index(drop=True)

    return df

def create_wordcloud(df: pd.DataFrame, user_name: str = '', option:str = 'no', src: str = ''):
    """
    function to create the wordcould
    df: pandas DataFrame
    user_name: name of the user if provided. If not then a random wordcould is generated
    option: with lemmatization or without (defualt: without)
    random: if random or for every data point
    """

    # check which wordcloud to create
    if (src == 'random'):
        df = create_random_df(df)
    if (src == 'user'):
        # filter DataFrame with user name
        df = df[df['user_name']==user_name]
        df = df.reset_index(drop=True)

    # remove links
    link_re = re.compile('http://\S+|https://\S+')
    str_user = ''

    for x in range(len(df)):
        str_ = df['full_text'][x]
        links_ = re.findall(link_re, str_)
    
        if (len(links_) == 1):
            str_ = str_.replace(links_[0], ' ')
        elif (len(links_) == 2):
            str_ = str_.replace(links_[0], '').replace(links_[1], '')
        elif (len(links_) == 3):
            str_ = str_.replace(links_[0], '').replace(links_[1], '').replace(links_[2], '')
        elif(len(links_) > 3):
            print('attention: more than 3 links in the tweet')
        elif (len(links_) == 0):
            pass
            
        str_user += ''.join(str_)

    # to lowercase
    str_user = str_user.lower()

    # remove hashtags
    hashtag_re = re.compile('#(\w+)')
    str_user = re.sub(hashtag_re, '', str_user)

    # tokenize
    tokens = word_tokenize(str_user)

    # remove non alphabetic Tokens
    words = [word for word in tokens if word.isalpha()]

    # remove stop words
    stop_words = set(stopwords.words('english'))
    # add misc words to stop words to enhance expressiveness
    misc_words = {"day", "week", "days"}
    stop_words.update(misc_words)
    words = [w for w in words if not w in stop_words]

    # remove words based on the tweets
    list_remove = ['round', 'today', 'yesterday', 'day', 'r2', 'amp']
    words = [w for w in words if not w in list_remove]

    # combine tokens to one string
    str_user = ''
    for w in words:
        word = w
        str_user += "".join(word)+ " "

    if option == 'no':
        ## create Wordcloud
        wordcloud = WordCloud(width=1200, height=600, background_color="white", collocations=False, scale=1.8).generate(str_user)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    elif option == 'yes':
        # Word cloud with lemmatizer
        wordnet_lemmatizer = WordNetLemmatizer()
        tokens = word_tokenize(str_user)
        str_user = ''
        for word in tokens:
            word_ = wordnet_lemmatizer.lemmatize(word, pos="v")
            str_user += "".join(word_)+ " "
        wordcloud = WordCloud(width=1200, height=600, background_color="white", collocations=False, scale=1.8).generate(str_user)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    # show details
    st.header('More information about the user')
    st.write(user_name)
    # Number of Tweets
    num_tweets = df.shape[0] 
    st.write('number of tweets: ', str(num_tweets))

    # First and last Tweet
    date_from_user = df['created_at'][0].split(" ")[0]
    date_to_user = df['created_at'][df.index[-1]].split(" ")[0]
    st.write('First Tweet: ', date_from_user, ' Last Tweet: ', date_to_user)

st.set_page_config(page_title="Wordcloud", page_icon="☁")
st.sidebar.header("Wordcloud")


# load data
@st.cache
def load_data(path):
    df = pd.read_csv(path) 
    return df

df = pd.read_csv('data/final/tweets_66DaysofData.csv')
rows = df.shape[0]
date_from = df['created_at'][0].split(" ")[0]
date_to = df['created_at'][df.index[-1]].split(" ")[0]

st.title('Word Cloud-Generator')
st.subheader('by Markus Müller ([@MarkusM99098101](https://twitter.com/MarkusM99098101))')

html_str = f"""
    This is a Word Cloud generator for the #66DaysofData Challenge. The Word Cloud is generated with the tweets form the 
    paricipant, when they used the above mentioned hashtag. 
    
    If you arent a participant and want to see different results you can try one of the following users: 
    KenJee\_DS, MarkusM99098101, KOrfanakis, \_paulo\_lopez\_, JackRaifer, or create a random one.

    The Word Cloud is created from a database with {rows} individual tweets ({date_from} to {date_to}).

    You can read more about the project on my [porfolio website](https://markusmueller-ds.github.io/portfolio/66days_analysis.html)
"""

st.markdown(html_str, unsafe_allow_html=True)
st.write("")

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def callback_wc():
    st.session_state.button_clicked = True

with st.sidebar:
    button_all_wc = st.button('Wordcloud')
    button_random_wc = st.button('Wordcloud Random')
    button_user_wc = st.button('Wordcloud User', on_click=callback_wc)

if (button_all_wc):
    st.write("Wordcloud for all")
    # show image of wordcloud
    # generte local

if (button_random_wc):
    st.write("Creating a Wordcloud for a random participant")
    df = load_data('data/final/tweets_66DaysofData.csv')
    create_wordcloud(df=df, src='random')

if (button_user_wc or st.session_state.button_clicked):
    option = st.selectbox('Do you want the Word Cloud with or without lemmatization?', ['no', 'yes']) 
    user_name = st.text_input('Twitter handle (without the @):')

    button_create_wc = st.button("Create Wordcloud")
    
    if(button_create_wc):
        st.write("Creating a Wordcoloud for a specific user")
        df = load_data('data/final/tweets_66DaysofData.csv')
        print(df.info())
        create_wordcloud(df=df, user_name=user_name, option=option, src="user")