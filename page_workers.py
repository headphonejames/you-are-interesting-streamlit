import streamlit as st
import constants
import crud_items_form_input
import util

def execute():
    st.title("Names of staff")
    crud_items_form_input.execute(
        df_key=constants.workers_dataframe_key_name,
        table_name=constants.workers_table_name,
        columns_names=constants.workers_config_columns_names,
        item_key_column_name=constants.workers_name,
        item_key=constants.workers_key,
        default_values={constants.worker_is_working:
                            {constants.default_value: False,
                             constants.is_display_column: False},
                        constants.timestamp_str:
                            {constants.is_display_column: False}
                        }
    )

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
