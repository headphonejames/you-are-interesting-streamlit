import streamlit as st
import constants
import crud_items_form_input

def execute():
    st.title("Prompts for connection")
    crud_items_form_input.execute(
        df_key=constants.prompts_dataframe_key_name,
        table_name=constants.prompts_table_name,
        columns_names=constants.prompts_config_columns_names,
        item_key_column_name=constants.prompts_key_column_name,
        item_key=constants.prompts_key,
        default_values={constants.timestamp_str:
                            {constants.is_display_column: False}
                        }
    )
