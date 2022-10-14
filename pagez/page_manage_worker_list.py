import streamlit as st
from constants import constants
from constants import workers
import lib.crud_items_form_input as crud_items_form_input

def execute():
    st.title("Names of staff")
    crud_items_form_input.execute(
        df_key=workers.df_key,
        table_name=workers.table_name,
        columns_names=workers.columns_names,
        item_key_column_name=workers.name,
        item_key=workers.name,
        default_values={workers.is_working:
                            {constants.default_value: False,
                             constants.is_display_column: False},
                        workers.log_index:
                            {constants.default_value: 1,
                             constants.is_display_column: False},
                        workers.timesheet_index:
                            {constants.default_value: 1,
                             constants.is_display_column: False},
                        workers.timestamp_str:
                            {constants.is_display_column: False}
                        }
    )
