from constants import constants
import streamlit as st
import xlsxwriter
from lib import google_sheets_funcs as gsheets
import datetime
from constants import pages
from constants import workers
from constants import shift
from constants import worker_log
from constants import prompts
from constants import connection



# getters and setters

def set_session_state_value(st, key, value):
    # print("set_session_state_value: {} {}".format(key, value))
    st.session_state[key] = value

def get_session_state_value(st, key, initValue=None):
    # print("get_session_state_value: {} {}".format(key, initValue))
    if key in st.session_state:
        # print("found {}".format(st.session_state[key]))
        return st.session_state[key]
    else:
        if initValue:
            # print("Init value {} {}".format(key, initValue))
            st.session_state[key] = initValue
        return initValue
    # otherwise force the exception
    raise Exception("AAAAAAA")

def update_current_page(page):
    st.session_state[pages.CURRENT_PAGE] = page

def get_current_page():
    return st.session_state[pages.CURRENT_PAGE]

def convert_to_boolean(value):
    if isinstance(value, bool):
        return value
    return not value.lower() == "false"

def get_worker_timesheet_table_name(worker_name):
    return worker_name + "-" + shift.timesheet_df_key

def get_worker_timesheet_df_key(worker_name):
    return worker_name + shift.timesheet_df_key

def get_worker_log_table_name(worker_name):
    return worker_name + "-" + worker_log.df_key

def get_worker_log_df_key(worker_name):
    return worker_name + worker_log.df_key

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
    return datetime.datetime.utcnow().replace(microsecond=0)

def str_timestamp():
    return timestamp().isoformat()

## flow functions
def update_connections(st, connection_obj):
    connections = get_session_state_value(st, connection.key)
    log_index = get_session_state_value(st, connection.index_key)
    connections[log_index] = connection_obj
    set_session_state_value(st, connection.key, connections)

def get_connection_from_cache(st):
    connections = get_session_state_value(st, connection.key)
    log_index = get_session_state_value(st, connection.index_key)
    if not log_index in connections:
        connections[log_index] = {}
    return connections[log_index]


def update_connection(st, key, value):
    connection = get_connection_from_cache(st)
    connection[key] = value
    update_connections(st, connection)

def connection_timestamp_update_db(st, column_name):
    # cache the timestamp
    now_datetime = timestamp()
    # update in db
    connection_update_current_connection_in_db(st, column_name, str(now_datetime))


def update_timestamp_timesheet_log(worker_name, worker_timesheet_index, column_name):
    return update_timesheet_log(worker_name, worker_timesheet_index, column_name, str_timestamp())

def update_timesheet_log(worker_name, worker_timesheet_index, column_name, value):
    # get timesheet worksheet
    timesheet_worksheet_df_key = get_worker_timesheet_df_key(worker_name)
    worksheets = get_session_state_value(st, constants.worksheets_df_key)
    timesheet_worksheet = worksheets[timesheet_worksheet_df_key]

    # get column for setting the stop time for the shift
    column_index = shift.column_names.index(column_name) + 1

    # put a value in that column
    gsheets.update_cell(worksheet=timesheet_worksheet,
                        row=worker_timesheet_index + 1,
                        column=column_index,
                        value=value)

def connection_start_persist_db(st):
    connection_timestamp_update_db(st, worker_log.time_contact)

def connection_start_time_update_db(st, end_timestamp_str, mins):
    timestamp_delta = datetime.timedelta(minutes=mins)
    endtime_timestamp = datetime.datetime.fromisoformat(end_timestamp_str)
    begin_timestamp = endtime_timestamp - timestamp_delta
    connection_update_current_connection_in_db(st, worker_log.time_contact, str(begin_timestamp))
    # also update prompt selection time if it exists
    prompt_timestamp = None
    if worker_log.time_prompt in get_connection_from_cache(st):
        prompt_timestamp = worker_log.time_prompt
    if prompt_timestamp:
        connection_update_current_connection_in_db(st, worker_log.time_prompt, str(begin_timestamp))

def connection_complete_persist_db(st):
    connection_timestamp_update_db(st, worker_log.time_finished)

def connection_update_current_connection_in_db(st, key, value):
    # update value in cache
    update_connection(st, key, value)

    # get worker name
    worker_name = get_session_state_value(st, workers.name_cached)
    # get the index in the log to update
    worker_log_index = get_session_state_value(st, workers.log_index)

    # get log worksheet
    log_worksheet_df_key = get_worker_log_df_key(worker_name)
    worksheets = get_session_state_value(st, constants.worksheets_df_key)
    log_worksheet = worksheets[log_worksheet_df_key]

    # get column for setting the stop time for the shift
    column_index = worker_log.column_names.index(key) + 1

    # create a timestamp in that column
    gsheets.update_cell(worksheet=log_worksheet,
                        row=worker_log_index + 1,
                        column=column_index,
                        value=value)

def complete_connection():
    connection_complete_persist_db(st)
    update_current_page(pages.CONNECTION_COMPLETE)

def bump_log_index():
    # get worker data
    workers_df = get_session_state_value(st, workers.df_key)

    # get the index in the log to update
    worker_log_index = get_session_state_value(st, workers.log_index)

    # update log index value in workers dataframe
    current_worker_row_index = get_session_state_value(st, constants.worker_index)
    workers_df.at[current_worker_row_index, workers.log_index]= worker_log_index + 1

    # update log index value in google sheet
    worksheets = get_session_state_value(st, constants.worksheets_df_key)
    workers_worksheet = worksheets[workers.df_key]
    worker_row_index = current_worker_row_index + 2
    # update workers log index in google sheet
    column_index = workers_df.columns.get_loc(workers.log_index) + 1
    gsheets.update_cell(worksheet=workers_worksheet,
                        row=worker_row_index,
                        column=column_index,
                        value=worker_log_index + 1)

    #bump index in cache
    # get the index in the log to update
    set_session_state_value(st, workers.log_index, worker_log_index + 1)


def return_to_waiting(st):
    connection_complete_persist_db(st)
    bump_log_index()
    update_current_page(pages.WAITING_FOR_FRIEND)

def reset_prompt_list(st):
    gsheets.reload_table(st, prompts.table_name, prompts.dataframe_key_name)
