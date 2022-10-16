import streamlit as st
import lib.util as util
from constants import pages

def execute():
    st.button("setup worker list", on_click=util.update_current_page, kwargs={"st": st, "page": pages.WORKERS})
    st.button("setup prompts list", on_click=util.update_current_page, kwargs={"st": st, "page": pages.PROMPTS})
    st.button("start shift", on_click=util.update_current_page, kwargs={"st": st, "page": pages.START_SHIFT})
