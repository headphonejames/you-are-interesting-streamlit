import streamlit as st
import lib.util as util
from constants import worker_log
from constants import constants
from constants import ratings
from constants import pages

def execute():
    is_show_slider_key = "show-slider"
    slider_key = "slider"
    is_show_slider = util.get_session_state_value(st, is_show_slider_key, False)

    def set_show_slider(value):
        util.set_session_state_value(st, is_show_slider_key, value)

    def all_done():
        # reset slider value
        util.set_session_state_value(st, is_show_slider_key, False)

        updated_connection_length = util.get_session_state_value(st, slider_key, 0)
        if updated_connection_length > 0:
            # reset connection start time
            # get endtime
            connection_cache = util.get_current_connection_from_cache(st)
            end_timestamp_str = connection_cache[worker_log.time_finished]
            util.connection_start_time_update_db(st, end_timestamp_str, updated_connection_length)

        notes = util.get_session_state_value(st, constants.notes_key)
        rating_str = util.get_session_state_value(st, constants.radio_str_key, "")
        rating_value = ratings.values_map[rating_str][ratings.value]
        util.connection_update_current_connection_in_db(st, worker_log.notes, notes)
        util.connection_update_current_connection_in_db(st, worker_log.rating, rating_value)
        # reset cached values
        util.set_session_state_value(st, constants.cached_notes_key, "")
        util.set_session_state_value(st, constants.connection_rating_radio_index_key, 0)
        util.return_to_waiting(st)

    def update_prompt():
        # cache the radio
        if constants.radio_str_key in st.session_state:
            rating_value = st.session_state[constants.radio_str_key]
            # translate that to radio index
            util.set_session_state_value(st,
                                         constants.connection_rating_radio_index_key,
                                         ratings.get_index_from_str(rating_value))
        notes = util.get_session_state_value(st, constants.notes_key, "")
        util.set_session_state_value(st, constants.cached_notes_key, notes)
        util.update_current_page(st, pages.CONNECTION_SELECT_PROMPT)

    st.title("Connection completed")
    # get cached info
    connection = util.get_current_connection_from_cache(st)
    # set the radio box
    radio_index = util.get_session_state_value(st, constants.connection_rating_radio_index_key, 0)
    st.radio("Rate the Connection", ratings.values, key=constants.radio_str_key, index=radio_index)
    prompt = "No prompt selected"
    if worker_log.prompt in connection:
        prompt = connection[worker_log.prompt]
    st.button("Prompt: {}".format(prompt), on_click=update_prompt)

    notes = util.get_session_state_value(st, constants.cached_notes_key, "")
    st.text_area("notes", key=constants.notes_key, value=notes)
    if not is_show_slider:
        st.button("update connection time", on_click=set_show_slider, args=(True, ))
    if is_show_slider:
        st.slider("connection length (minutes)", min_value=0, max_value=20, value=5, step=1, key=slider_key)

    st.button("done", on_click=all_done)