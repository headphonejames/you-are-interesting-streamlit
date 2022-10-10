import streamlit as st
import constants
import lib.util as util
from lib import google_sheets_funcs as gsheets

def reset_cache(worker_name, worker_timesheet_index, worker_log_index, worker_sheet_index):
    # clear connections cache
    util.set_session_state_value(st, constants.connections_key, {})

    #cache worker name
    util.set_session_state_value(st, constants.workers_name_cached, worker_name)

    #cache current worker timesheet index
    util.set_session_state_value(st, constants.worker_timesheet_index, worker_timesheet_index)

    #cachec current worker log index
    util.set_session_state_value(st, constants.worker_log_index, worker_log_index)

    # cache prompts if not already in df
    util.get_persisted_data(constants.prompts_dataframe_key_name, constants.prompts_table_name)

    # cache the worker's worker sheet index
    util.set_session_state_value(st, constants.worker_index, worker_sheet_index)

    # initialize dataframe for worker timesheet
    worker_timesheet_df_key = util.get_worker_timesheet_df_key(worker_name)
    worker_timesheet_table = util.get_worker_timesheet_table_name(worker_name)
    # create worker timesheet if not exists, otherwise load it
    if worker_timesheet_df_key not in st.session_state:
        gsheets.load_table(st=st,
                           table_name=worker_timesheet_table,
                           df_key_name=worker_timesheet_df_key,
                           createTable=True,
                           columns=constants.worker_shift_column_names)

    # initialize dataframe for worker log
    worker_log_df_key = util.get_worker_log_df_key(worker_name)
    worker_log_table = util.get_worker_log_table_name(worker_name)
    # create worker log if not exists, otherwise load it
    if worker_log_df_key not in st.session_state:
        gsheets.load_table(st=st,
                           table_name=worker_log_table,
                           df_key_name=worker_log_df_key,
                           createTable=True,
                           columns=constants.worker_log_column_names)

def start_shift(worker_name, worker_timesheet_index, worker_log_index, worker_sheet_index):
    reset_cache(worker_name, worker_timesheet_index, worker_log_index, worker_sheet_index)

    # get worker data
    workers_df = util.get_session_state_value(st, constants.workers_df_key)

    # get worksheet for workers
    worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
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
    util.set_session_state_value(st, constants.workers_df_key, workers_df)

    # initialize dataframe for worker timesheet
    worker_timesheet_df_key = util.get_worker_timesheet_df_key(worker_name)
    # get worker timesheet sheet
    worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
    worksheet = worksheets[worker_timesheet_df_key]
    # add a row to the timesheet sheet
    column_values = ["", ""]
    gsheets.insert_row(worksheet=worksheet, column_values=column_values)
    # insert the correct time
    util.update_timestamp_timesheet_log(worker_name, worker_timesheet_index, constants.worker_shift_start)

    # cache the worker's worker sheet index
    util.set_session_state_value(st, constants.worker_index, worker_sheet_index)

    # go to waiting_for_friend
    util.update_current_page(constants.WAITING_FOR_FRIEND)

def resume_shift(worker_name, worker_timesheet_index, worker_log_index, worker_sheet_index):
    reset_cache(worker_name, worker_timesheet_index, worker_log_index, worker_sheet_index)
    # go to waiting_for_friend
    util.update_current_page(constants.WAITING_FOR_FRIEND)


def execute():
    util.init_table(constants.workers_df_key, constants.workers_table_name, constants.workers_config_columns_names)
    workers_working = []

    df = util.get_session_state_value(st, constants.workers_df_key)
    for index, row in df.iterrows():
        worker_name = row[constants.workers_name]
        worker_timesheet_index = row[constants.worker_timesheet_index]
        worker_log_index = row[constants.worker_log_index]
        is_working =  util.convert_to_boolean(row[constants.worker_is_working])
        if not is_working:
            st.button(worker_name, key="id_{}".format(worker_name),
                      on_click = start_shift,
                      args=(worker_name, int(worker_timesheet_index),
                            int(worker_log_index), index, ))
        else:
            workers_working.append(worker_name)

    if len(workers_working) > 0:
        st.write("resume active shift")
        for index, row in df.iterrows():
            worker_name = row[constants.workers_name]
            worker_timesheet_index = row[constants.worker_timesheet_index]
            worker_log_index = row[constants.worker_log_index]
            is_working =  util.convert_to_boolean(row[constants.worker_is_working])
            if is_working:
                st.button(worker_name, key="id_{}".format(worker_name),
                          on_click = resume_shift,
                          args=(worker_name, int(worker_timesheet_index),
                                int(worker_log_index), index, ))

    st.button("back to main", on_click=util.update_current_page, kwargs={"page": constants.ENRTY})