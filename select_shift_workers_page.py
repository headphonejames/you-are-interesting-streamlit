import streamlit as st
import constants
import select_items_list
import util

workers_table_name = "workers"
workers_label_name = "workers"
workers_column_name = "workers"
workers_dataframe_key_name = "workers_dataframe"
item_name = "workers"
worker_input_key = "workers_input"

def execute():
    st.title("Pick who is working this shift")
    select_items_list.execute(workers_dataframe_key_name,
                      workers_table_name,
                      workers_label_name,
                      workers_column_name,
                      item_name,
                      worker_input_key,
                      constants.WORKERS_LIST)
    st.button("start shift", on_click=util.update_state, args=constants.WORKERS)
    st.button("return to main", on_click=util.update_state, kwargs={"page": constants.ENRTY})


