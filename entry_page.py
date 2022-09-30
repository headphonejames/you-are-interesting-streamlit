import streamlit as st
import util
import constants
def execute():
    st.button("setup worker list", on_click=util.update_state, kwargs={"page": constants.workers_table})
    st.button("start shift", on_click=util.update_state, kwargs={"page": constants.START_SHIFT} )
