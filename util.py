import constants
import streamlit as st

def update_state(page):
    st.session_state[constants.CURRENT_PAGE] = page
