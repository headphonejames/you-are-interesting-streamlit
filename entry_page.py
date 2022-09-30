import streamlit as st
import util
import constants
def execute():
    st.button("setup worker list", on_click=util.update_current_page, kwargs={"page": constants.WORKERS})
    st.button("start shift", on_click=util.update_current_page, kwargs={"page": constants.START_SHIFT})
