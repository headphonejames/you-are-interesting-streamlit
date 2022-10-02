import streamlit as st
import constants
import util
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func
import datetime

def start_shift(worker_name, index):
    # get worker data
    workers_df = df_func.get_session_state_value(st, constants.workers_dataframe_key_name)
    #cache worker name
    df_func.set_session_state_value(st, constants.workers_name, worker_name)
    # get worksheet
    worksheet = df_func.get_session_state_value(st, constants.worksheet_key)
    # update "isworking" value
    workers_df.at[index,constants.worker_is_working]= True
    # get the column index for "isworking"
    column_index = workers_df.columns.get_loc(constants.worker_is_working) + 1
    # update just those cells in the worksheet
    # index add 2 (starts at 1, +1  for headers)
    gsheets.update_cell(worksheet=worksheet,
                        row=index+2,
                        column=column_index,
                        value=True)
    # update the cached dataframe
    df_func.set_session_state_value(st, constants.workers_dataframe_key_name, workers_df)

    # initialize dataframe for worker timesheet
    df_key = worker_name + constants.worker_timesheet_df_key
    table_name = worker_name + "-" + constants.worker_timesheet_df_key

    if df_key not in st.session_state:
        gsheets.load_or_create_the_table(table_name, df_key, constants.worker_timesheet_column_names)

    df = df_func.get_session_state_value(st, df_key)
    # add start time to sheet
    df.loc[len(df.index)] = [datetime.datetime.now(), 0]
    # update the google sheet
    gsheets.create_or_update_the_table(dataframe=df, table_name=table_name)

    # go to waiting_for_friend
    util.update_current_page(constants.WAITING_FOR_FRIEND)

def execute():
    # initialize dataframe
    if constants.workers_dataframe_key_name not in st.session_state:
        gsheets.load_or_create_the_table(constants.workers_table_name,
                                         constants.workers_dataframe_key_name,
                                         constants.workers_config_columns_names)

    df = df_func.get_session_state_value(st, constants.workers_dataframe_key_name)

    for index, row in df.iterrows():
        worker_name = row[constants.workers_name]
        is_working =  util.convert_to_boolean(row[constants.worker_is_working])
        if not is_working:
            st.button(worker_name, key="id_{}".format(worker_name),
                      on_click = start_shift,
                      args=(worker_name, index, ))

    st.button("back to main", on_click=util.update_current_page, kwargs={"page": constants.ENRTY})