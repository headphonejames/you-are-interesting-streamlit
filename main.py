import streamlit as st
import constants
from pagez import page_select_current_worker, \
    page_entry, page_prompts, \
    page_manage_worker_list, page_waiting_for_friend, \
    page_connection_completed, page_connection_begins, page_connection_select_prompt, \
    page_connection_happening

# init current page state
if constants.CURRENT_PAGE not in st.session_state:
    st.session_state[constants.CURRENT_PAGE] = constants.ENRTY

current_page = st.session_state[constants.CURRENT_PAGE]

if current_page == constants.ENRTY:
    page_entry.execute()
elif current_page == constants.WORKERS:
    page_manage_worker_list.execute()
elif current_page == constants.PROMPTS:
    page_prompts.execute()
elif current_page == constants.START_SHIFT:
    page_select_current_worker.execute()
elif current_page == constants.WAITING_FOR_FRIEND:
    page_waiting_for_friend.execute()
elif current_page == constants.CONNECTION_BEGINS:
    page_connection_begins.execute()
elif current_page == constants.CONNECTION_SELECT_PROMPT:
    page_connection_select_prompt.execute()
elif current_page == constants.CONNECTION_HAPPENING:
    page_connection_happening.execute()
elif current_page == constants.CONNECTION_COMPLETE:
    page_connection_completed.execute()