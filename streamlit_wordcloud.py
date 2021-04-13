import numpy as np
import pandas as pd
import streamlit as st
import re
import matplotlib.pyplot as plt 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

# load data
df = pd.read_csv('data/final/Tweets_wc.csv') 

st.header('WordCloud-Generator')

user_name = st.text_input('Twitter user Name: ')
# st.write(f'WordCloud wird für {user_name} erstellt')

if(st.button('Create WordCloud')):
    # FILTER DATAFRAME WITH USER NAME  
    df_user = df[df['user_name']==user_name]
    df_user.reset_index(inplace=True)

    # REMOVE LINKS
    link_re = re.compile('http://\S+|https://\S+')
    str_user = ''

    for x in range(len(df_user)):
        str_ = df_user['full_text'][x]
        links_ = re.findall(link_re, str_)
    
        if (len(links_) == 1):
            str_ = str_.replace(links_[0], ' ')
        elif (len(links_) == 2):
            str_ = str_.replace(links_[0], '').replace(links_[1], '')
        elif (len(links_) == 3):
            str_ = str_.replace(links_[0], '').replace(links_[1], '').replace(links_[2], '')
        elif(len(links_) > 3):
            print('error: more than 3 links in the tweet')
        elif (len(links_) == 0):
            pass
            
        str_user += ''.join(str_)

    # TO LOWERCASE
    str_user = str_user.lower()

    # REMOVE HASHTAGS
    hashtag_re = re.compile('#(\w+)')
    str_user = re.sub(hashtag_re, '', str_user)

    # TOKENIZE
    tokens = word_tokenize(str_user)

    # REMOVE NON ALPHABETIC TOKES
    words = [word for word in tokens if word.isalpha()]

    # REMOVE STOP WORDS
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    # REMOVE WORDS BASED ON THE TWEETS
    list_remove = ['round', 'today', 'yesterday', 'day', 'r2', 'amp']
    words = [w for w in words if not w in list_remove]

    # COMBINE TOKENS TO ONE STRING
    str_user = ''
    for w in words:
        word = w
        str_user += "".join(word)+ " "

    ## CREATE WORDCLOUD
    wordcloud = WordCloud(width=1200, height=600, background_color="white", collocations=False, scale=1.8).generate(str_user)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)