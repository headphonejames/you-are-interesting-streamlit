import streamlit as st

from constants import constants
from constants import pages
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func
import lib.util as util

def execute(df_key, table_name, columns_names, item_key_column_name, item_key, default_values, unit_name):
    util.init_table(df_key, table_name, columns_names)
    util.init_value(constants.modded_key, False)
    util.init_value(constants.ui_input_data, {})

    index = 0
    df = util.get_session_state_value(st, df_key)

    def clear_state(modded):
        # reset values
        st.session_state[constants.ui_input_data] = {}
        st.session_state[constants.modded_key] = modded
        # clear out ui values
        for column_name in columns_names:
            if not column_name in default_values:
                st.session_state[column_name] = ''

    def remove_item(item, index):
        new_df = df_func.remove_row(df, index)
        util.set_session_state_value(st, df_key, new_df)
        st.session_state[constants.modded_key] = True

    def update_text(column_name):
        text_input = st.session_state[column_name]
        st.session_state[constants.ui_input_data][column_name] = text_input

    def add_items(df):
        data = st.session_state[constants.ui_input_data]
        name = data[item_key]
        # check if name already in table
        if not df[item_key].astype("object").str.contains(name).any():
            # fill out default values
            for column_name in columns_names:
                if column_name in default_values and constants.default_value in default_values[column_name]:
                    data[column_name] = default_values[column_name][constants.default_value]
            # add a timestamp to this row
            data[constants.timestamp_str] = util.timestamp()
            #update datatable
            df = df_func.add_row(df, data)
            util.set_session_state_value(st, df_key, df)
            clear_state(True)

    if item_key_column_name in df:
        for item in df[item_key_column_name]:
            index = index + 1
            st.checkbox(item, key="id_{}".format(item),  on_change=remove_item, args=(item, index, ))

    for column_name in columns_names:
        if column_name in default_values:
            if default_values[column_name][constants.is_display_column]:
                value = st.session_state[column_name]
                st.text_input(label=column_name, value=value, on_change=update_text, key=column_name, args=(column_name,))
        else:
            value = ''
            if column_name in st.session_state:
                value = st.session_state[column_name]
            st.text_input(label=column_name, value=value, on_change=update_text, key=column_name, args=(column_name,))

    st.button(label="add {}".format(unit_name), on_click=add_items, args=(df, ))

    def done(commit=False):
        # update sheet
        if commit:
            df = gsheets.create_or_update_the_table(util.get_session_state_value(st, df_key), table_name)
            # cache the df
            util.set_session_state_value(st=st, key=df_key, value=df)
        clear_state(False)
        util.update_current_page(page=pages.ENRTY)

    if st.session_state[constants.modded_key]:
        st.button("Commit to db and return to main", on_click=done, args=(True, ))
    st.button("return to main", on_click=done, args=(False, ))

