import constants
import streamlit as st
import xlsxwriter
from lib import google_sheets_funcs as gsheets
import datetime

# getters and setters

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

def get_current_page():
    return st.session_state[constants.CURRENT_PAGE]

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

# utility functions

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

def timestamp():
    return datetime.datetime.now().replace(microsecond=0)

def str_timestamp():
    return str(timestamp())

## flow functions

def connection_timestamp_update_db(st, key, column_name):
    # cache the starttime
    now_datetime = timestamp()
    set_session_state_value(st, key, now_datetime)
    # update in db
    connection_update_current_connection_in_db(column_name, str(now_datetime))


def connection_start_persist_db(st):
    connection_timestamp_update_db(st, constants.start_timestamp_key, constants.worker_log_time_contact)

def connection_start_time_update_db(endtime_timestamp, mins):
    timestamp_delta = datetime.timedelta(minutes=mins)
    print(timestamp_delta)
    print(endtime_timestamp)
    print("aSDf")
    begin_timestamp = endtime_timestamp - timestamp_delta
    print(begin_timestamp)
    connection_update_current_connection_in_db(constants.worker_log_time_contact, str(begin_timestamp))

def connection_complete_persist_db(st):
    connection_timestamp_update_db(st, constants.end_timestamp_key, constants.worker_log_time_finished)

def connection_update_current_connection_in_db(column, value):
    # update google sheets with completed time
    # get worker name
    worker_name = get_session_state_value(st, constants.workers_name_cached)
    # get the index in the log to update
    worker_log_index = get_session_state_value(st, constants.worker_log_index)

    # get log worksheet
    log_worksheet_df_key = get_worker_log_df_key(worker_name)
    worksheets = get_session_state_value(st, constants.worksheets_df_key)
    log_worksheet = worksheets[log_worksheet_df_key]

    # get column for setting the stop time for the shift
    column_index = constants.worker_log_column_names.index(column) + 1

    # create a timestamp in that column
    gsheets.update_cell(worksheet=log_worksheet,
                        row=worker_log_index + 1,
                        column=column_index,
                        value=value)

def bump_log_index():
    # get worker data
    workers_df = get_session_state_value(st, constants.workers_df_key)

    # get the index in the log to update
    worker_log_index = get_session_state_value(st, constants.worker_log_index)

    # update log index value in workers dataframe
    current_worker_row_index = get_session_state_value(st, constants.worker_index)
    workers_df.at[current_worker_row_index,constants.worker_log_index]= worker_log_index + 1

    # update log index value in google sheet
    worksheets = get_session_state_value(st, constants.worksheets_df_key)
    workers_worksheet = worksheets[constants.workers_df_key]
    worker_row_index = current_worker_row_index + 2
    # update workers log index in google sheet
    column_index = workers_df.columns.get_loc(constants.worker_log_index) + 1
    gsheets.update_cell(worksheet=workers_worksheet,
                        row=worker_row_index,
                        column=column_index,
                        value=worker_log_index + 1)

    #bump index in cache
    # get the index in the log to update
    set_session_state_value(st, constants.worker_log_index, worker_log_index + 1)


def return_to_waiting(st):
    connection_complete_persist_db(st)
    bump_log_index()
    update_current_page(constants.WAITING_FOR_FRIEND)

def reset_prompt_list(st):
    gsheets.reload_table(st, constants.prompts_table_name, constants.prompts_dataframe_key_name)
