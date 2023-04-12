import streamlit as st
import nltk

# st-pages to rename the pages on the sidebar
# https://github.com/blackary/st_pages

# Downlad NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

st.set_page_config(
    page_title="66DaysofData Dashboard"
)

st.write("# 66DaysofData Dashboard")

st.markdown(
    """
    This an app based on streamlit to showcase various analysis of the 66DaysofData tweets.

    ### How to use?
    - Select topic from the sidebar on the left (if sidebar is not showing click on the arrow in the left upper corner)
    - Choose ganularity of analysis (for all, for a specific user, or random)


    You can read more about the project on my [porfolio website](https://markusmueller-ds.github.io/portfolio/66days_analysis.html) or
    visit the repo on [Github](https://github.com/MarkusMueller-DS/66DaysofData-tweets)
    """
)