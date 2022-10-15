import streamlit as st
import lib.util as util
from constants import constants
from constants import pages
from constants import workers
from constants import worker_log
from constants import ratings
from lib import google_sheets_funcs as gsheets

def execute():
    def begin_contact():
        #update value in log
        # get worker name
        worker_name = util.get_session_state_value(st, workers.name_cached)
        # get log worksheet
        log_worksheet_df_key = util.get_worker_log_df_key(worker_name)
        worksheets = util.get_session_state_value(st, constants.worksheets_df_key)
        log_worksheet = worksheets[log_worksheet_df_key]

        # get column for setting the stop time for the shift
        columns = ["", "", "", "", 0, ""]
        # add it to the sheet
        gsheets.append_row(worksheet=log_worksheet,
                           values=columns)
        # update starttime
        # TODO fix update datetime afterwards for consistent data format
        util.connection_start_persist_db(st)
        util.update_current_page(pages.CONNECTION_BEGINS)

    def return_to_previous_connection():
        # set index to previous index
        previous_connection = util.undo_finish_previous_connection(st)
        # reset notes
        util.set_session_state_value(st, constants.notes_key, previous_connection[worker_log.notes])
        # reset rating
        rating_value = previous_connection[worker_log.rating]
        # translate that to radio index
        util.set_session_state_value(st, constants.connection_rating_radio_index_key, ratings.get_index_from_value(rating_value))
        # return to connection complete page
        util.update_current_page(pages.CONNECTION_COMPLETE)

    worker_name = util.get_session_state_value(st, workers.name_cached)
    st.title("{}: Waiting for friend".format(worker_name))
    st.button("Contact initiated", on_click = begin_contact)
    st.button("Reload Prompts", on_click= util.reset_prompt_list, args=(st, ))
    # check if there is a previous connection
    if util.is_prev_connection(st):
        st.button("Update previous connection", on_click = return_to_previous_connection)
    st.button("Finish shift", key="finished", on_click = util.update_current_page, kwargs={"page": pages.FINISH_SHIFT})