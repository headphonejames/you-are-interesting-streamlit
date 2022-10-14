import streamlit as st
import lib.util as util
from constants import pages
from constants import worker_log
from constants import prompts

def execute():
    def connection_happening(prompt):
        # set prompt time
        util.connection_timestamp_update_db(st, worker_log.time_prompt)
        # put prompt in df and db
        util.connection_update_current_connection_in_db(st, worker_log.prompt, prompt)
        util.update_current_page(pages.CONNECTION_HAPPENING)

    st.title("Prompts for connection")
    # get prompts
    prompts_list = util.get_persisted_data(prompts.dataframe_key_name, prompts.table_name)
    st.button("other", on_click=connection_happening, args=("other", ))

    for index, row in prompts_list.iterrows():
        prompt = row[prompts.column_name]
        st.button(prompt, on_click=connection_happening, key=index, args=(prompt, ))

    st.button("connection complete", on_click=util.complete_connection)