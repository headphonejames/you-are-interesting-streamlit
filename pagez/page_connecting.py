import streamlit as st
import lib.util as util
import constants
from lib import google_sheets_funcs as gsheets
import datetime

def execute():
    # get worker name
    worker_name = util.get_session_state_value(st, constants.workers_name_cached)

    # get the index in the log to update
    worker_log_index = util.get_session_state_value(st, constants.worker_log_index)

    # update row with connection time
    # get log worksheet
    log_worksheet_df_key = util.get_worker_log_df_key(worker_name)
    worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
    log_worksheet = worksheets[log_worksheet_df_key]

    # get column for setting the stop time for the shift
    column_index = constants.worker_log_column_names.index(constants.worker_log_time_contact) + 1

    # create a timestamp in that column
    gsheets.update_cell(worksheet=log_worksheet,
                        row=worker_log_index + 1,
                        column=column_index,
                        value=str(datetime.datetime.now()))


st.button("select prompt", on_click=util.update_current_page, kwargs={"page": constants.PROMPTS})
st.button("connection complete", on_click=util.update_current_page, kwargs={"page": constants.WAITING_FOR_FRIEND})
