import streamlit as st
import lib.util as util
import constants
def execute():
    def all_done():
        notes = util.get_session_state_value(st, constants.notes_key)
        rating = util.get_session_state_value(st, constants.rating_key, 0)
        util.connection_update_current_connection_in_db(constants.worker_log_notes, notes)
        util.connection_update_current_connection_in_db(constants.worker_log_rating, rating)
        util.return_to_waiting()

    def update_rating(rating):
        util.set_session_state_value(st, constants.rating_key, rating)

    st.title("Connection completed")
    # hack for no 5 star rating system
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        st.button('1', on_click=update_rating, args=(1,))
    with col2:
        st.button('2', on_click=update_rating, args=(2,))
    with col3:
        st.button('3', on_click=update_rating, args=(3,))
    with col4:
        st.button('4', on_click=update_rating, args=(4,))
    with col5:
        st.button('5', on_click=update_rating, args=(5,))

    st.text_area("notes", key=constants.notes_key)
    st.button("done", on_click=all_done)