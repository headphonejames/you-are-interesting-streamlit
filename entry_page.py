import streamlit as st
import util
import constants
def execute():
    st.button("setup worker list", on_click=util.update_state, kwargs={"page": constants.WORKERS} )
    st.button("select shift workers", on_click=util.update_state, kwargs={"page": constants.SETUP_SHIFT_WORKERS} )
    st.button("start shift", on_click=util.update_state, kwargs={"page": constants.WORKERS} )
