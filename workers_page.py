import streamlit as st
import constants
import crud_items_list
import util

def execute():
    st.title("Names of staff")
    crud_items_list.execute(
        df_key=constants.workers_dataframe_key_name,
        table_name=constants.workers_table_name,
        label_name=constants.workers_label_name,
        column_name=constants.workers_column_name,
        item_name=constants.workers_item_name,
        item_key=constants.worker_input_key)

    st.button("return to main", on_click=util.update_current_page, kwargs={"page": constants.ENRTY})


# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
