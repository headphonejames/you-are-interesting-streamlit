import streamlit as st
import lib.util as util

def execute():
    st.button("connection finished", on_click=util.complete_connection)
