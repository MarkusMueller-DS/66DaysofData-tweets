import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud


def replace_links(df:pd.DataFrame) -> str:
    """
    Funciton to replace links
    """
    link_re = re.compile('http://\S+|https://\S+')
    str_global = ''

    for x in range(len(df.iloc[:100,])):
        str_ = df['full_text'][x]
        re_ = re.sub(link_re, '', str_)
        str_global += re_ + ' ' 

    return str_global

def add_lemmatization(corpus: str) -> str:
    """
    Function to lemmatize a text corpus
    """
    wordnet_lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(corpus)
    str_lemma = ''
    for word in tokens:
        word_ = wordnet_lemmatizer.lemmatize(word, pos="v")
        str_lemma += "".join(word_)+ " "

    return str_lemma

def create_wordcloud(df: pd.DataFrame):
    """
    function to create the wordcould
    df: pandas DataFrame
    """
    
    # remove links from tweets
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

    print("creating Wordcloud")

    """
    if option == 'no':
        ## create Wordcloud
        wordcloud = WordCloud(width=1200, height=600, background_color="white", collocations=False, scale=1.8).generate(str_user)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
    """
    str_global = add_lemmatization(corpus)

    wordcloud = WordCloud(width=1200, height=600, background_color="white", collocations=False, scale=1.8).generate(str_global)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    wordcloud.to_file('reports/figures/wordcloud.png')


# load data
PATH_DATA = 'data/final/tweets_66DaysofData.csv'
df = pd.read_csv(PATH_DATA)

create_wordcloud(df)