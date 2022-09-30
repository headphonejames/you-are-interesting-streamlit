import streamlit as st
import constants
import entry_page
import workers_page
import select_shift_workers_page

# init current page state
if constants.CURRENT_PAGE not in st.session_state:
    st.session_state[constants.CURRENT_PAGE] = constants.ENRTY

current_page = st.session_state[constants.CURRENT_PAGE]

if current_page == constants.ENRTY:
    entry_page.execute()
elif current_page == constants.WORKERS:
    workers_page.execute()
elif current_page == constants.SETUP_SHIFT_WORKERS:
    select_shift_workers_page.execute()
