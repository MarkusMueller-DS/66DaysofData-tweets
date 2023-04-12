import pandas as pd
import streamlit as st
import re
import random
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
from create_wc_global import replace_links


def create_random_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to create a DataFrame with tweets from a random participant
    df: main DataFrame with every tweet
    """
    #print("create wordcloud for random user")
    # find random user 
    unique_user = df['user_id'].unique()
    random_user_id = random.choice(unique_user)
    user_name = df[df['user_id'] == random_user_id]['user_name'].values[0]
    st.markdown(f"### Creating a Wordcloud for a {user_name}")

    df = df[df['user_name']==user_name]
    df = df.reset_index(drop=True)

    return df

def create_wordcloud(df: pd.DataFrame, user_name: str = '', option:str = 'no', src: str = ''):
    """
    function to create the wordcould
    df: pandas DataFrame
    user_name: name of the user if provided. if not then a random wordcould is generated
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

    corpus = replace_links(df)

    # to lowercase
    corpus = corpus.lower()

    # remove hashtags
    hashtag_re = re.compile('#(\w+)')
    corpus = re.sub(hashtag_re, '', corpus)

    # tokenize
    tokens = word_tokenize(corpus)

    # remove non alphabetic Tokens
    words = [word for word in tokens if word.isalpha()]

    # remove stop words
    stop_words = set(stopwords.words('english'))
    # add misc words to stop words to enhance expressiveness
    misc_words = {"day", "week", "days", "round", "today", "yesterday", "r2", "amp"}
    stop_words.update(misc_words)
    words = [w for w in words if not w in stop_words]

    # combine tokens to one string
    corpus = ''
    for w in words:
        word = w
        corpus += "".join(word)+ " "

    if option == 'no':
        ## create Wordcloud
        wordcloud = WordCloud(width=1200, height=600, background_color="white", collocations=False, scale=1.8).generate(corpus)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    elif option == 'yes':
        # Word cloud with lemmatizer
        wordnet_lemmatizer = WordNetLemmatizer()
        tokens = word_tokenize(corpus)
        str_global = ''
        for word in tokens:
            word_ = wordnet_lemmatizer.lemmatize(word, pos="v")
            str_global += "".join(word_)+ " "
        wordcloud = WordCloud(width=1200, height=600, background_color="white", collocations=False, scale=1.8).generate(str_global)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    # show details
    st.markdown('#### More information about the participant')
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
@st.cache_data
def load_data(path) -> pd.DataFrame:
    df = pd.read_csv(path) 
    return df

df = pd.read_csv('data/final/tweets_66DaysofData.csv')
rows = df.shape[0]
date_from = df['created_at'][0].split(" ")[0]
date_to = df['created_at'][df.index[-1]].split(" ")[0]

st.title('Word Cloud-Generator')
#st.subheader('by Markus Müller ([@MarkusM99098101](https://twitter.com/MarkusM99098101))')

html_str = f"""
    This is a Word Cloud generator for the #66DaysofData Challenge. The Word Cloud is generated from the participants tweets
    , when they used the above mentioned hashtag. 
    
    If you aren't a participant and want to see different results you can try one of the following users: 
    KenJee\_DS, MarkusM99098101, KOrfanakis, \_paulo\_lopez\_, JackRaifer, or create a random one (select Wordcould Random from the sidebar).

    The Word Cloud is created from a database with {rows} individual tweets ({date_from} to {date_to}).

"""

st.markdown(html_str, unsafe_allow_html=True)
st.write("")

# init Session States
# https://docs.streamlit.io/library/advanced-features/session-state#initialization
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
if "user" not in st.session_state:
    st.session_state.user = False

def callback_wc():
    st.session_state.button_clicked = True

with st.sidebar:
    button_all_wc = st.button('Wordcloud')
    button_random_wc = st.button('Wordcloud Random')
    button_user_wc = st.button('Wordcloud Participant', on_click=callback_wc)

if (button_all_wc):
    print(st.session_state)
    st.write("Wordcloud for the entire dataset:")
    # show image of wordcloud
    st.image('reports/figures/wordcloud.png')

if (button_random_wc):
    # set session state to not show elements form participant wordcloud
    st.session_state.user = False
    print(st.session_state)
    df = load_data('data/final/tweets_66DaysofData.csv')
    create_wordcloud(df=df, src='random')

if (button_user_wc or st.session_state.button_clicked or st.session_state.user):
    st.session_state.user = True
    print(st.session_state)
    option = st.selectbox('Do you want the Word Cloud with or without lemmatization?', ['no', 'yes']) 
    user_name = st.text_input('Twitter handle (without the @):')

    button_create_wc = st.button("Create Wordcloud")
    
    if(button_create_wc):
        print(st.session_state)
        st.markdown(f"### Creating a Wordcoloud for {user_name}")
        df = load_data('data/final/tweets_66DaysofData.csv')
        create_wordcloud(df=df, user_name=user_name, option=option, src="user")
        st.session_state.button_clicked = False
        print(st.session_state)