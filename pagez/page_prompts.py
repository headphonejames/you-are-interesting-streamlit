import streamlit as st
from constants import constants
from constants import prompts
import lib.crud_items_form_input as crud_items_form_input

def execute():
    st.title("Prompts for connection")
    crud_items_form_input.execute(
        df_key=prompts.dataframe_key_name,
        table_name=prompts.table_name,
        columns_names=prompts.config_columns_names,
        item_key_column_name=prompts.key_column_name,
        item_key=prompts.key,
        default_values={constants.timestamp_str:
                            {constants.is_display_column: False}
                        }
    )
