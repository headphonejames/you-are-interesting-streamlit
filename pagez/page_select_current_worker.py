import streamlit as st
import constants
import util
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func
import datetime

def start_shift(worker_name, worker_timesheet_index, worker_sheet_index):
    # get worker data
    workers_df = df_func.get_session_state_value(st, constants.workers_df_key)
    #cache worker name
    df_func.set_session_state_value(st, constants.workers_name, worker_name)
    #cache current worker timesheet index
    df_func.set_session_state_value(st, constants.worker_timesheet_index, worker_timesheet_index)

    # get timesheet worksheet
    worksheets = df_func.get_session_state_value(st, constants.worksheets_df_key)
    worksheet = worksheets[constants.workers_df_key]

    # update "isworking" value
    workers_df.at[worker_sheet_index, constants.worker_is_working]= True
    # get the column index for "isworking"
    column_index = workers_df.columns.get_loc(constants.worker_is_working) + 1
    # set is working to "true" in workers sheet
    gsheets.update_cell(worksheet=worksheet,
                        row=worker_sheet_index + 2,
                        column=column_index,
                        value=True)
    # update the cached dataframe
    df_func.set_session_state_value(st, constants.workers_df_key, workers_df)

    # initialize dataframe for worker timesheet
    worker_timesheet_df_key = util.get_worker_timesheet_df_key(worker_name)
    worker_timesheet_table = util.get_worker_timesheet_table_name(worker_name)
    # create worker timesheet if not exists, otherwise load it
    if worker_timesheet_df_key not in st.session_state:
        gsheets.load_or_create_the_table(st=st,
                                         table_name=worker_timesheet_table,
                                         df_key_name=worker_timesheet_df_key,
                                         columns=constants.worker_shift_column_names)

    # add start time to sheet

    # get worker timesheet sheet
    worksheets = df_func.get_session_state_value(st, constants.worksheets_df_key)
    worksheet = worksheets[worker_timesheet_df_key]
    # add a row to the timesheet sheet
    column_values = [str(datetime.datetime.now()), ""]
    gsheets.insert_row(worksheet=worksheet, column_values=column_values)

    # cache the worker's worker sheet index
    df_func.set_session_state_value(st, constants.worker_index, worker_sheet_index)
    # go to waiting_for_friend
    util.update_current_page(constants.WAITING_FOR_FRIEND)

def execute():
    # initialize dataframe
    if constants.workers_df_key not in st.session_state:
        gsheets.load_or_create_the_table(st=st,
                                         table_name=constants.workers_table_name,
                                         df_key_name=constants.workers_df_key,
                                         columns=constants.workers_config_columns_names)
    df = df_func.get_session_state_value(st, constants.workers_df_key)
    st.write(df)
    for index, row in df.iterrows():
        worker_name = row[constants.workers_name]
        worker_timesheet_index = row[constants.worker_timesheet_index]
        is_working =  util.convert_to_boolean(row[constants.worker_is_working])
        if not is_working:
            st.button(worker_name, key="id_{}".format(worker_name),
                      on_click = start_shift,
                      args=(worker_name, int(worker_timesheet_index), index, ))

    st.button("back to main", on_click=util.update_current_page, kwargs={"page": constants.ENRTY})