import streamlit as st
import lib.util as util
import constants
def execute():
    st.button("setup worker list", on_click=util.update_current_page, kwargs={"page": constants.WORKERS})
    st.button("setup prompts list", on_click=util.update_current_page, kwargs={"page": constants.PROMPTS})
    st.button("start shift", on_click=util.update_current_page, kwargs={"page": constants.START_SHIFT})
