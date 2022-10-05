import streamlit as st
import lib.util as util
import constants

def execute():
    st.title("Prompts for connection")
    # get prompts
    prompts = util.get_persisted_data(constants.prompts_dataframe_key_name, constants.prompts_table_name)
    st.button("other")
    for prompt in prompts:
        st.button(prompt)