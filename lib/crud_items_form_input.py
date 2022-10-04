import streamlit as st

import constants
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func
import datetime
import lib.util as util

def execute(df_key, table_name, columns_names, item_key_column_name, item_key, default_values):
    def clear_state(modded):
        # intialize session state data obj
        st.session_state[constants.st_data_key] = {}
        # pre-fill sessions state data obj with any default values
        for column_name in columns_names:
            if column_name in default_values and constants.default_value in default_values[column_name]:
                st.session_state[constants.st_data_key][column_name] = default_values[column_name][constants.default_value]
            else:
                # just set as empty
                st.session_state[column_name] = ''
        st.session_state[constants.modded_key] = modded

    if constants.modded_key not in st.session_state:
        clear_state(False)

    # initialize dataframe
    if df_key not in st.session_state:
        gsheets.load_or_create_the_table(st=st,
                                         table_name=table_name,
                                         df_key_name=df_key,
                                         columns=columns_names)

    def remove_item(item, index):
        df = util.get_session_state_value(st, df_key)
        #Remove item from list in data table
        new_df = df_func.remove_col(df, index)
        util.set_session_state_value(st, df_key, new_df)
        st.session_state[constants.modded_key] = True
        # set_df(st, df_func.remove_col(df_func.get_df(st, df_key), index))

    def update_text(column_name):
        text_input = st.session_state[column_name]
        st.session_state[constants.st_data_key][column_name] = text_input

    def add_items():
        data = st.session_state[constants.st_data_key]
        df = util.get_session_state_value(st, df_key)
        name = data[item_key]
        # check if name already in table
        if not df[item_key].astype("object").str.contains(name).any():
            # add a timestamp to thie row
            data[constants.timestamp_str] = datetime.datetime.now()
            #update datatable
            df = df_func.add_row(df, data)
            util.set_session_state_value(st, df_key, df)
            clear_state(True)

    index = 0
    df = util.get_session_state_value(st, df_key)

    if item_key_column_name in df:
        for item in df[item_key_column_name]:
            index = index + 1
            st.checkbox(item, key="id_{}".format(item),  on_change=remove_item, args=(item, index, ))

    for column_name in columns_names:
        if column_name in default_values:
            if default_values[column_name][constants.is_display_column]:
                st.text_input(label=column_name, value=st.session_state[column_name], on_change=update_text, key=column_name, args=(column_name,))
        else:
            value = ''
            if column_name in st.session_state:
                value = st.session_state[column_name]
            st.text_input(label=column_name, value=value, on_change=update_text, key=column_name, args=(column_name,))

    st.button(label="add {}".format(table_name), on_click=add_items)

    def done(commit=False):
        # update sheet
        if st.session_state[constants.modded_key]:
            if commit:
                gsheets.create_or_update_the_table(util.get_session_state_value(st, df_key), table_name)
            st.session_state[constants.modded_key] = False

        # clear all state
        clear_state(modded=False)

        util.update_current_page(page=constants.ENRTY)

    if st.session_state[constants.modded_key]:
        st.button("Commit to db and return to main", on_click=done, args=(True, ))
    st.button("return to main", on_click=done, args=(False, ))

