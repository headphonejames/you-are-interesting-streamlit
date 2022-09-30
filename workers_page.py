import streamlit as st
import constants
import crud_items_list
import util

workers_table_name = "workers"
workers_label_name = "workers"
workers_column_name = "workers"
workers_dataframe_key_name = "workers_dataframe"
item_name = "workers"
worker_input_key = "workers_input"

def execute():
    st.title("Names of staff")
    crud_items_list.execute(
        df_key=workers_dataframe_key_name,
        table_name=workers_table_name,
        label_name=workers_label_name,
        column_name=workers_column_name,
        item_name=item_name,
        item_key=worker_input_key)

    st.button("return to main", on_click=util.update_state, kwargs={"page": constants.ENRTY})


# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
