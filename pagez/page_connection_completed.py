import streamlit as st
import lib.util as util
from constants import worker_log

radio_str_key = "radio-key"
notes_key = "notes"

fun_str = "fun!"
pretty_fun_str = "pretty fun"
ok_str = "ok"
not_fun_str = "not fun"
ineffective_str = "ineffective"
unrated_str = "unrated"

values = [unrated_str, fun_str, pretty_fun_str, ok_str, not_fun_str, ineffective_str]
values_map = {unrated_str: 0,
              fun_str: 5,
              pretty_fun_str: 4,
              ok_str: 3,
              not_fun_str: 2,
              ineffective_str: 1}

def execute():
    is_show_slider_key = "show-slider"
    slider_key = "slider"

    is_show_slider = util.get_session_state_value(st, is_show_slider_key, False)

    def set_show_slider(value):
        util.set_session_state_value(st, is_show_slider_key, value)

    def all_done():
        rating_str = util.get_session_state_value(st, radio_str_key, 0)
        rating_value = values_map[rating_str]


        # reset slider value
        util.set_session_state_value(st, is_show_slider_key, False)

        updated_connection_length = util.get_session_state_value(st, slider_key, 0)
        if updated_connection_length > 0:
            # reset connection start time
            # get endtime
            connection_cache = util.get_connection_from_cache(st)
            end_timestamp_str = connection_cache[worker_log.time_finished]
            util.connection_start_time_update_db(st, end_timestamp_str, updated_connection_length)

        notes = util.get_session_state_value(st, notes_key)
        util.connection_update_current_connection_in_db(st, worker_log.notes, notes)
        util.connection_update_current_connection_in_db(st, worker_log.rating, rating_value)
        util.return_to_waiting(st)


    st.title("Connection completed")
    st.radio("Rate the Connection", values, key=radio_str_key)


    st.text_area("notes", key=notes_key)
    if not is_show_slider:
        st.button("update connection time", on_click=set_show_slider, args=(True, ))
    if is_show_slider:
        st.slider("connection length (minutes)", min_value=0, max_value=20, value=5, step=1, key=slider_key)

    st.button("done", on_click=all_done)