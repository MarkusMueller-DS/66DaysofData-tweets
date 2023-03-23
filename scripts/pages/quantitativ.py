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
    df = load_data('data/final/tweets_66DaysofData.csv')

    n_tweets = df.shape[0]
    date_from = df['created_at'][0].split(' ')[0]
    date_to = df['created_at'][df.index[-1]].split(' ')[0]
    participants = df['user_id'].nunique()

    top_5_participants = df.groupby('user_name')['user_id'].count().sort_values(ascending=False).head(5)

    length = df["full_text"].apply(len)
    mean_len = length.mean()
    max_len = length.max()
    min_len = length.min()
    median_len = length.median()

    basic_str = f"""
        ### Basics quantitative stats
        - **{n_tweets}** tweets from #66DaysofData collected
        - Tweets from **{date_from}** to **{date_to}** 
        - **{participants}** unique participants took part in the challenge 

        ### Top 5 participants
        1. {top_5_participants.index[0]} with {top_5_participants.values[0]} tweets
        2. {top_5_participants.index[1]} with {top_5_participants.values[1]} tweets
        3. {top_5_participants.index[2]} with {top_5_participants.values[2]} tweets
        4. {top_5_participants.index[3]} with {top_5_participants.values[3]} tweets
        5. {top_5_participants.index[4]} with {top_5_participants.values[4]} tweets

        ### Tweets
        - Average length of a tweet: {mean_len:.2f} 
        - Max length: {max_len}
        - Min length: {min_len}
        - Median langth: {median_len} 
    """
    st.markdown(basic_str, unsafe_allow_html=True)


    # plots
    df_plot = df[["created_at", "tweet_id"]]
    df_plot['created_at'] = pd.to_datetime(df_plot['created_at'])
    df_plot['date'] = [d.date() for d in df_plot['created_at']]
    df_plot['time'] = [d.time() for d in df_plot['created_at']]
    df_plot.drop(['created_at'], axis=1, inplace=True)

    # group by date and count number of tweets on that day
    countTweetsDay = df_plot.groupby(['date']).count()['tweet_id']
    countTweetsDay = pd.DataFrame(countTweetsDay)
    countTweetsDay.rename(columns={'tweet_id': 'count'}, inplace=True)

    # make sure that tweet sum is equal
    assert countTweetsDay['count'].sum() == df.shape[0], "should be equal"

    countTweetsDay.reset_index(inplace=True)

    st.markdown('### Plot of the tweets')
    st.bar_chart(data=countTweetsDay, x="date", y="count", use_container_width=True)
    st.markdown("""
        Ther are four peaks clearly visible. This corresponds with the 
        4 Rounds of the #66DaysofDataChallenge.
    """)


if (button_random_qa):
    st.write("Statistics for random participant")

if (button_user_qa or st.session_state.button_clicked_qa):
    user_name = st.text_input('Twitter handle (without the @):')

    button_create_qa = st.button("get stats")
    
    if(button_create_qa):
        st.write("Statistics for specific user")