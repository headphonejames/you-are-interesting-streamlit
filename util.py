import constants
import streamlit as st
import xlsxwriter

def update_current_page(page):
    st.session_state[constants.CURRENT_PAGE] = page

def convert_to_boolean(value):
    if isinstance(value, bool):
        return value
    return not value.lower() == "false"

def get_worker_timesheet_table_name(worker_name):
    return worker_name + "-" + constants.worker_timesheet_df_key

def get_worker_timesheet_df_key(worker_name):
    return worker_name + constants.worker_timesheet_df_key

def get_column_google_name(column_index):
    return xlsxwriter.utility.xl_col_to_name(column_index)