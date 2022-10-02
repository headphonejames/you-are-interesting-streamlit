import streamlit as st
import constants
import crud_items_list
import util

def execute():
    st.title("Prompts for connection")
    crud_items_list.execute(
        df_key=constants.prompts_dataframe_key_name,
        table_name=constants.prompts_table_name,
        label_name=constants.prompts_label_name,
        column_name=constants.prompts_column_name,
        item_name=constants.prompts_item_name)

    st.button("return to main", on_click=util.update_current_page, kwargs={"page": constants.ENRTY})


# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()