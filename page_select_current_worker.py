import streamlit as st
import constants
import util
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func

def start_shift(worker, index):
    print(worker)
    # create table if does not already exist
    # go to waiting_for_friend

def execute():
    # initialize dataframe
    if constants.workers_dataframe_key_name not in st.session_state:
        df = gsheets.load_or_create_the_table(constants.workers_table_name, ["name", "contact"])
        df_func.set_df(st, constants.workers_dataframe_key_name, df)

    index = 0
    df = df_func.get_df(st, constants.workers_dataframe_key_name)

    if constants.workers_item_name in df:
        for item in df[constants.workers_item_name]:
            index = index + 1
            st.button(item, key="id_{}".format(item), on_click = start_shift, args=(item, index, ))

    st.button("back to main", on_click=util.update_current_page, kwargs={"page": constants.ENRTY})