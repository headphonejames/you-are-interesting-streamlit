import streamlit as st
import lib.util as util
import constants

def execute():
    def complete_connection():
        util.connection_complete_update_db()
        util.update_current_page(constants.CONNECTION_COMPLETE)

    st.button("connection finished", on_click=complete_connection)
