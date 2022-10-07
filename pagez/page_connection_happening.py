import streamlit as st
import lib.util as util
import constants

def execute():
    def complete_connection():
        util.connection_complete_persist_db(st)
        util.update_current_page(constants.CONNECTION_COMPLETE)

    st.button("connection finished", on_click=complete_connection)
