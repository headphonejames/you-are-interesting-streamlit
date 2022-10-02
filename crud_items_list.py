import streamlit as st

import util
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func
import constants

def execute(df_key, table_name, label_name, column_name, item_name):
    #constants
    if 'modded' not in st.session_state:
        st.session_state.modded = False

    # initialize dataframe
    if df_key not in st.session_state:
        gsheets.load_or_create_the_table(table_name, [column_name])

    def remove_item(item, index):
        df = df_func.get_session_state_value(st, df_key)
        #Remove item from list in data table
        new_df = df_func.remove_col(df, index)
        df_func.set_session_state_value(st, df_key, new_df)
        st.session_state.modded = True
        # set_df(st, df_func.remove_col(df_func.get_df(st, df_key), index))

    def clear_state(df):
        df_func.set_session_state_value(st, df_key, df)
        st.session_state[column_name] = ''
        st.session_state.modded = True

    def add_item():
        df = df_func.get_session_state_value(st, df_key)
        item = st.session_state[column_name]
        # check if items already exists
        if not item in df[column_name].tolist():
            #update datatable
            df = df_func.add_row(df, [item])
            clear_state(df)

    index = 0
    df = df_func.get_session_state_value(st, df_key)

    if item_name in df:
        for item in df[item_name]:
            index = index + 1
            st.checkbox(item, key="id_{}".format(item),  on_change=remove_item, args=(item, index, ))

    st.session_state.item_name = ''
    st.text_input(label='', placeholder=label_name, on_change=add_item, key=column_name)

    def done():
        # update sheet
        if st.session_state.modded:
            gsheets.create_of_update_the_table(df_func.get_session_state_value(st, df_key), table_name)
            st.session_state.modded = False
        util.update_current_page(page=constants.ENRTY)

    st.button("return to main", on_click=done)
