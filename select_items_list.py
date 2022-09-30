import streamlit as st
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func

def execute(df_key, table_name, label_name, column_name, item_name, item_key, session_list_key):
    # initialize dataframe
    if df_key not in st.session_state:
        df_func.set_df(st, df_key, gsheets.load_the_table(table_name))

    # init list in session if not exists
    if session_list_key not in st.session_state:
        st.session_state[session_list_key] = []

    # initialize items list
    if not column_name in df_func.get_df(st, df_key):
        # add item column to datatable
        updated_df = df_func.get_df(st, df_key)[column_name] = []
        df_func.set_df(st, df_key, updated_df)

    def clear_state(df):
        df_func.set_df(st, df_key, df)
        st.session_state[item_key] = ''

    def toggle_item(item, index):
        list_from_session = st.session_state[session_list_key]
        if not item in list_from_session:
            list_from_session.append(item)

    index = 0
    df = df_func.get_df(st, df_key)

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
