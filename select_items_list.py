import streamlit as st
from lib import google_sheets_funcs as gsheets
from lib import util as util

def execute(df_key, table_name, column_name, item_name, session_list_key):
    # initialize dataframe
    if df_key not in st.session_state:
        gsheets.load_or_create_the_table(st=st,
                                         table_name=table_name,
                                         df_key_name=df_key,
                                         columns=[column_name])

    # init list in session if not exists
    if session_list_key not in st.session_state:
        st.session_state[session_list_key] = []

    # initialize items list
    if not column_name in util.get_session_state_value(st, df_key):
        # add item column to datatable
        updated_df = util.get_session_state_value(st, df_key)[column_name] = []
        util.set_session_state_value(st, df_key, updated_df)

    def toggle_item(item, index):
        list_from_session = st.session_state[session_list_key]
        if not item in list_from_session:
            list_from_session.append(item)

    index = 0
    df = util.get_session_state_value(st, df_key)

    list_from_session = st.session_state[session_list_key]

    if item_name in df:
        for item in df[item_name]:
            index = index + 1
            checked = item in list_from_session
            st.checkbox(item,
                        value=checked,
                        key="id_{}".format(item),
                        on_change=toggle_item,
                        args=(item, index, ) )
