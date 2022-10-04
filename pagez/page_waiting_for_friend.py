import streamlit as st
import lib.util as util
import constants
from lib import google_sheets_funcs as gsheets
import datetime

def execute():
    def finish_shift():
        # get worker name
        worker_name = util.get_session_state_value(st, constants.workers_name)
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
                    value=str(datetime.datetime.now()))

        # change isWorking to false and update timesheet index

        # initialize dataframe if not there
        if constants.workers_df_key not in st.session_state:
            gsheets.load_or_create_the_table(st=st,
                                             table_name=constants.workers_table_name,
                                             df_key_name=constants.workers_df_key,
                                             columns=constants.worker_column_names)
        # get worker data
        workers_df = util.get_session_state_value(st, constants.workers_df_key)

        # update "isworking" value to false in workers dataframe
        worker_sheet_index = util.get_session_state_value(st, constants.worker_index)
        workers_df.at[worker_sheet_index,constants.worker_is_working]= False

        # update the timesheet index in workers dataframe
        workers_df.at[worker_sheet_index,constants.worker_timesheet_index] = worker_timesheet_index + 1
        workers_df.reset_index(drop=True)

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


    st.write("Waiting for friend")
    worker_name = util.get_session_state_value(st, constants.workers_name)
    st.write("worker_name {}".format(worker_name))

    st.write(st.session_state)
    df = util.get_session_state_value(st, constants.workers_df_key)
    st.write(df)
    st.button("Contact initiated")
    st.button("Finish shift", key="finished", on_click = finish_shift)