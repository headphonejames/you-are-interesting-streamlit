import streamlit as st
import lib.util as util
from constants import constants
from constants import pages
from constants import workers
from constants import shift
from constants import connection
from lib import google_sheets_funcs as gsheets

def execute():
    def finish_shift():
        # get worker name
        worker_name = util.get_session_state_value(st, workers.name_cached)
        # get the index in the timesheet to update
        worker_timesheet_index = util.get_session_state_value(st, workers.timesheet_index)
        # update the worker shift time
        util.update_timestamp_timesheet_log(worker_name, worker_timesheet_index, shift.stop)

        # change isWorking to false and update timesheet index
        # get worker data
        workers_df = util.get_session_state_value(st, workers.df_key)

        # update "isworking" value to false in workers dataframe
        worker_sheet_index = util.get_session_state_value(st, constants.worker_index)
        workers_df.at[worker_sheet_index, workers.is_working]= False

        # update the timesheet index in workers dataframe
        workers_df.at[worker_sheet_index, workers.timesheet_index] = worker_timesheet_index + 1

        # update "isworking" in google sheet to false
        column_index = workers_df.columns.get_loc(workers.is_working) + 1
        worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
        workers_worksheet = worksheets[workers.df_key]
        worker_google_sheet_index = worker_sheet_index + 2
        gsheets.update_cell(worksheet=workers_worksheet,
                            row=worker_google_sheet_index,
                            column=column_index,
                            value=False)

        # update workers timesheet index in google sheet
        column_index = workers_df.columns.get_loc(workers.timesheet_index) + 1
        gsheets.update_cell(worksheet=workers_worksheet,
                            row=worker_google_sheet_index,
                            column=column_index,
                            value=worker_timesheet_index + 1)


        # update the cached dataframe
        util.set_session_state_value(st, workers.df_key, workers_df)
        # go to entry page
        util.update_current_page(pages.ENRTY)

    def begin_contact():
        #update value in log
        # get worker name
        worker_name = util.get_session_state_value(st, workers.name_cached)

        # get the index in the log to update
        worker_log_index = util.get_session_state_value(st, workers.log_index)

        # cache the log index
        util.set_session_state_value(st, connection.index_key, worker_log_index)

        # get log worksheet
        log_worksheet_df_key = util.get_worker_log_df_key(worker_name)
        worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
        log_worksheet = worksheets[log_worksheet_df_key]

        # get column for setting the stop time for the shift
        columns = ["", "", "", "", "", 0, ""]
        # add it to the sheet
        gsheets.append_row(worksheet=log_worksheet,
                           values=columns)
        # update starttime
        # TODO fix update datetime afterwards for consistent data format
        util.connection_start_persist_db(st)

    util.update_current_page(pages.CONNECTION_BEGINS)

    worker_name = util.get_session_state_value(st, workers.name_cached)
    st.title("{}: Waiting for friend".format(worker_name))
    st.button("Contact initiated", on_click = begin_contact)
    st.button("Reload Prompts", on_click= util.reset_prompt_list, args=(st, ))
    st.button("Finish shift", key="finished", on_click = finish_shift)