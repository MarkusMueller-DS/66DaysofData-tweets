import streamlit as st

# st-pages to rename the pages on the sidebar
# https://github.com/blackary/st_pages

st.set_page_config(
    page_title="66DaysofData Dashboard"
)

st.write("# 66DaysofData Dashboard")

st.sidebar.success("Select part of analysis")

st.markdown(
    """
    This an app based on streamllit to showcase various analysis of the 66DaysofData tweets.
    Select intersting parts from the sidebar on the left.
    """
)