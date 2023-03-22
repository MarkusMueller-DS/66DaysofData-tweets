import streamlit as st
import pandas as pd

# load data
@st.cache
def load_data(path):
    df = pd.read_csv(path) 
    return df

st.set_page_config("Quantitative Analysis")
st.sidebar.header("Quantitative Analysis")


df = load_data('data/final/tweets_66DaysofData.csv')
st.title("Quantitative Analysis")
st.write(
    """
    Quantitative analysis of the tweets
    """
)

if "button_clicked_qa" not in st.session_state:
    st.session_state.button_clicked_qa = False

def callback_qa():
    st.session_state.button_clicked_qa = True

with st.sidebar:
    button_all_qa = st.button('Stats for all')
    button_random_qa = st.button('Stats for random')
    button_user_qa = st.button('Stats for user', on_click=callback_qa)

if (button_all_qa):
    st.write("Statistics for all")
    # show image of wordcloud
    # generte local

if (button_random_qa):
    st.write("Statistics for random participant")

if (button_user_qa or st.session_state.button_clicked_qa):
    user_name = st.text_input('Twitter handle (without the @):')

    button_create_qa = st.button("get stats")
    
    if(button_create_qa):
        st.write("Statistics for specific user")