import constants
import streamlit as st
import xlsxwriter
from lib import google_sheets_funcs as gsheets

def set_session_state_value(st, key, value):
    print("set_session_state_value: {} {}".format(key, value))
    st.session_state[key] = value

def get_session_state_value(st, key, initValue=None):
    print("get_session_state_value: {} {}".format(key, initValue))
    if key in st.session_state:
        print("found {}".format(st.session_state[key]))
        return st.session_state[key]
    else:
        if initValue:
            print("Init value {} {}".format(key, initValue))
            st.session_state[key] = initValue
        return initValue
    # otherwise force the exception
    raise Exception("AAAAAAA")

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

def get_worker_log_table_name(worker_name):
    return worker_name + "-" + constants.worker_log_df_key

def get_worker_log_df_key(worker_name):
    return worker_name + constants.worker_log_df_key


def get_column_google_name(column_index):
    return xlsxwriter.utility.xl_col_to_name(column_index)

def get_persisted_data(df_key, table_name):
    if df_key not in st.session_state:
        gsheets.load_table(st=st,
                           table_name=table_name,
                           df_key_name=df_key,
                           createTable=False)

    return get_session_state_value(st, df_key)

def init_value(key, defaultValue):
    if not key in st.session_state:
        st.session_state[key] = defaultValue


def init_table(key, table_name, column_names):
    if key not in st.session_state:
        gsheets.load_table(st=st,
                           table_name=table_name,
                           df_key_name=key,
                           createTable=True,
                           columns=column_names)
