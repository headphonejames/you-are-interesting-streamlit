import streamlit as st
import lib.util as util
import constants
from lib import google_sheets_funcs as gsheets
import datetime

def execute():
    def return_to_waiting():
        # update google sheets with completed time
        # get worker name
        worker_name = util.get_session_state_value(st, constants.workers_name_cached)
        # get the index in the log to update
        worker_log_index = util.get_session_state_value(st, constants.worker_log_index)

        # get log worksheet
        log_worksheet_df_key = util.get_worker_log_df_key(worker_name)
        worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
        log_worksheet = worksheets[log_worksheet_df_key]

        # get column for setting the stop time for the shift
        column_index = constants.worker_log_column_names.index(constants.worker_log_time_finished) + 1

        # create a timestamp in that column
        gsheets.update_cell(worksheet=log_worksheet,
                            row=worker_log_index + 1,
                            column=column_index,
                            value=str(datetime.datetime.now()))

        # bump index in other sheet + df

        # change isWorking to false and update timesheet index
        # get worker data
        workers_df = util.get_session_state_value(st, constants.workers_df_key)

        # update log index value in workers dataframe
        current_worker_row_index = util.get_session_state_value(st, constants.worker_index)
        workers_df.at[current_worker_row_index,constants.worker_log_index]= worker_log_index + 1

        # update log index value in google sheet
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
        util.set_session_state_value(st, constants.worker_log_index, worker_log_index + 1)

        util.update_current_page(constants.WAITING_FOR_FRIEND)

    st.button("select prompt", on_click=util.update_current_page, kwargs={"page": constants.PROMPTS})
    st.button("connection complete", on_click=return_to_waiting)
