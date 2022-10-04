import streamlit as st
import util
import constants
import lib.df_funcs as df_funcs
import constants
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func
import datetime

def execute():
    # create table if necessary to start shift
    # create table if track interactions
    def finish_shift():
        # get worker name
        worker_name = df_func.get_session_state_value(st, constants.workers_name)
        # get the index in the timesheet to update
        worker_timesheet_index = df_func.get_session_state_value(st, constants.worker_timesheet_index)
        # get timesheet worksheet
        timesheet_worksheet_df_key = util.get_worker_timesheet_df_key(worker_name)
        worksheets = df_func.get_session_state_value(st, constants.worksheets_df_key)
        timesheet_worksheet = worksheets[timesheet_worksheet_df_key]
        # get column for stopping the shift
        column_index = constants.worker_shift_column_names.index(constants.worker_shift_stop) + 1
        # update the timestmpae
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
        workers_df = df_func.get_session_state_value(st, constants.workers_df_key)

        # update "isworking" value to false in workers dataframe
        worker_sheet_index = df_func.get_session_state_value(st, constants.worker_index)
        workers_df.at[worker_sheet_index,constants.worker_is_working]= False

        # update the timesheet index in workers dataframe
        workers_df.at[worker_sheet_index,constants.worker_timesheet_index] = worker_timesheet_index + 1
        workers_df.reset_index(drop=True)

        # update "isworking" in google sheet
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
        df_func.set_session_state_value(st, constants.workers_df_key, workers_df)
        # go to entry page
        util.update_current_page(constants.ENRTY)


    st.write("Waiting for friend")
    df = df_func.get_session_state_value(st, constants.workers_df_key)
    # st.write(df)
    st.button("Finish shift", key="finished", on_click = finish_shift)