import streamlit as st
import lib.util as util
from constants import constants
from constants import pages

def execute():
    st.button("select prompt", on_click=util.update_current_page, kwargs={"page": pages.CONNECTION_SELECT_PROMPT})
    st.button("connection complete", on_click=util.complete_connection)
