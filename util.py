import constants
import streamlit as st

def update_current_page(page):
    st.session_state[constants.CURRENT_PAGE] = page
