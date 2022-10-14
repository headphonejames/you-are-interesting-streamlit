import streamlit as st
import lib.util as util
from constants import constants
from constants import pages
from constants import workers
from constants import shift
from lib import google_sheets_funcs as gsheets

notes_key = "notes"


def execute():
    def finish_shift():
        # get worker name
        worker_name = util.get_session_state_value(st, workers.name_cached)
        # get the index in the timesheet to update
        worker_timesheet_index = util.get_session_state_value(st, workers.timesheet_index)
        # update the worker shift time
        util.update_timestamp_timesheet_log(worker_name, worker_timesheet_index, shift.stop)
        # update the notes for this shift
        notes = util.get_session_state_value(st, notes_key)
        util.update_timesheet_log(worker_name, worker_timesheet_index, shift.notes, notes)

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

    st.text_area("how do you feel?", key=notes_key)
    st.button("done", on_click=finish_shift)