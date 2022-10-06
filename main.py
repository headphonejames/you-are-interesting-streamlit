import streamlit as st
import constants

# init current page state
if constants.CURRENT_PAGE not in st.session_state:
    st.session_state[constants.CURRENT_PAGE] = constants.ENRTY

current_page_key = st.session_state[constants.CURRENT_PAGE]
constants.map[current_page_key].execute()