import numpy as np
import pandas as pd
import streamlit as st
import re
import matplotlib.pyplot as plt
# import nltk_download_utils
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud

# load data
df = pd.read_csv('data/final/Tweets_wc.csv')

st.title('Word Cloud-Generator')
st.subheader('by Markus Müller ([@MarkusM99098101](https://twitter.com/MarkusM99098101))')

st.markdown("""
    This is a Word Cloud generator for the #66DaysofData Challenge. The Word Cloud is generated with the tweets form the 
    paricipant, when they used the above mentioned hashtag. 
    
    If you arent a participant and want to see different results you can try one of the following users: 
    KenJee_DS, MarkusM99098101, KOrfanakis, _paulo_lopez_, JackRaifer.
""")

st.write("")

option = st.selectbox('Do you want the Word Cloud with or without lemmatization?', ['no', 'yes']) 

user_name = st.text_input('Twitter user Name (without the @):')
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

    if option == 'no':
        ## CREATE WORDCLOUD
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
        