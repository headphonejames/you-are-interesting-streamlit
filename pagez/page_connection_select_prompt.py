import streamlit as st
import lib.util as util
import constants

def execute():
    def connection_happening(prompt):
        # put prompt in df and db
        util.connection_update_current_connection_in_db(constants.worker_log_prompt, prompt)
        util.update_current_page(constants.CONNECTION_HAPPENING)

    st.title("Prompts for connection")
    # get prompts
    prompts = util.get_persisted_data(constants.prompts_dataframe_key_name, constants.prompts_table_name)
    st.button("other", on_click=connection_happening, args=("other", ))

    for index, row in prompts.iterrows():
        prompt = row[constants.prompts_column_name]
        st.button(prompt, on_click=connection_happening, key=index, args=(prompt, ))

    st.button("connection complete", on_click=util.return_to_waiting)