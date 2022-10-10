import streamlit as st
import lib.util as util
import constants
from lib import google_sheets_funcs as gsheets

def execute():
    def finish_shift():
        # get worker name
        worker_name = util.get_session_state_value(st, constants.workers_name_cached)
        # get the index in the timesheet to update
        worker_timesheet_index = util.get_session_state_value(st, constants.worker_timesheet_index)

        # get timesheet worksheet
        timesheet_worksheet_df_key = util.get_worker_timesheet_df_key(worker_name)
        worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
        timesheet_worksheet = worksheets[timesheet_worksheet_df_key]

        # get column for setting the stop time for the shift
        column_index = constants.worker_shift_column_names.index(constants.worker_shift_stop) + 1

        # create a timestamp in that column
        gsheets.update_cell(worksheet=timesheet_worksheet,
                    row=worker_timesheet_index + 1,
                    column=column_index,
                    value=util.str_timestamp())

        # change isWorking to false and update timesheet index
        # get worker data
        workers_df = util.get_session_state_value(st, constants.workers_df_key)

        # update "isworking" value to false in workers dataframe
        worker_sheet_index = util.get_session_state_value(st, constants.worker_index)
        workers_df.at[worker_sheet_index,constants.worker_is_working]= False

        # update the timesheet index in workers dataframe
        workers_df.at[worker_sheet_index,constants.worker_timesheet_index] = worker_timesheet_index + 1

        # update "isworking" in google sheet to false
        column_index = workers_df.columns.get_loc(constants.worker_is_working) + 1
        workers_worksheet = worksheets[constants.workers_df_key]
        worker_google_sheet_index = worker_sheet_index + 2
        gsheets.update_cell(worksheet=workers_worksheet,
                            row=worker_google_sheet_index,
                            column=column_index,
                            value=False)

        # update workers timesheet index in google sheet
        column_index = workers_df.columns.get_loc(constants.worker_timesheet_index) + 1
        gsheets.update_cell(worksheet=workers_worksheet,
                            row=worker_google_sheet_index,
                            column=column_index,
                            value=worker_timesheet_index + 1)


        # update the cached dataframe
        util.set_session_state_value(st, constants.workers_df_key, workers_df)
        # go to entry page
        util.update_current_page(constants.ENRTY)

    def begin_contact():
        #update value in log
        # get worker name
        worker_name = util.get_session_state_value(st, constants.workers_name_cached)

        # get the index in the log to update
        worker_log_index = util.get_session_state_value(st, constants.worker_log_index)

        # cache the log index
        util.set_session_state_value(st, constants.connection_index_key, worker_log_index)

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

    util.update_current_page(constants.CONNECTION_BEGINS)

    worker_name = util.get_session_state_value(st, constants.workers_name_cached)
    st.title("{}: Waiting for friend".format(worker_name))
    st.button("Contact initiated", on_click = begin_contact)
    st.button("Reload Prompts", on_click= util.reset_prompt_list, args=(st, ))
    st.button("Finish shift", key="finished", on_click = finish_shift)