import streamlit as st
import lib.util as util
import constants

def execute():
    st.button("select prompt", on_click=util.update_current_page, kwargs={"page": constants.CONNECTION_SELECT_PROMPT})
    st.button("connection complete", on_click=util.return_to_waiting)
