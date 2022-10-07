import streamlit as st
import lib.util as util
import constants
def execute():
    is_show_slider_key = "show-slider"
    slider_key = "slider"

    is_show_slider = util.get_session_state_value(st, is_show_slider_key, False)

    def set_show_slider(value):
        util.set_session_state_value(st, is_show_slider_key, value)

    def all_done():
        connection_length = util.get_session_state_value(st, slider_key, 0)
        if connection_length > 0:
            # reset connection start time
            # get endtime
            end_timestamp = util.get_session_state_value(st, constants.end_timestamp_key)
            print(end_timestamp)
            util.connection_start_time_update_db(end_timestamp, connection_length)

        notes = util.get_session_state_value(st, constants.notes_key)
        rating = util.get_session_state_value(st, constants.rating_key, 0)
        util.connection_update_current_connection_in_db(constants.worker_log_notes, notes)
        util.connection_update_current_connection_in_db(constants.worker_log_rating, rating)
        util.return_to_waiting(st)

    def update_rating(rating):
        util.set_session_state_value(st, constants.rating_key, rating)

    st.title("Connection completed")
    # hack for no 5 star rating system
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        st.button('fun!', on_click=update_rating, args=(5,))
    with col2:
        st.button('pretty fun', on_click=update_rating, args=(4,))
    with col3:
        st.button('ok', on_click=update_rating, args=(3,))
    with col4:
        st.button('not fun', on_click=update_rating, args=(2,))
    with col5:
        st.button('ineffective', on_click=update_rating, args=(1,))

    st.text_area("notes", key=constants.notes_key)
    if not is_show_slider:
        st.button("update connection time", on_click=set_show_slider, args=(True, ))
    if is_show_slider:
        st.slider("connection length", min_value=0, max_value=20, value=5, step=1, key=slider_key)

    st.button("done", on_click=all_done)