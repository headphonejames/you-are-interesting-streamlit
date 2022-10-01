import streamlit as st
import constants
import page_entry
import page_workers
import page_select_current_worker
import page_prompts

# init current page state
if constants.CURRENT_PAGE not in st.session_state:
    st.session_state[constants.CURRENT_PAGE] = constants.ENRTY

current_page = st.session_state[constants.CURRENT_PAGE]

if current_page == constants.ENRTY:
    page_entry.execute()
elif current_page == constants.WORKERS:
    page_workers.execute()
elif current_page == constants.PROMPTS:
    page_prompts.execute()
elif current_page == constants.START_SHIFT:
    page_select_current_worker.execute()