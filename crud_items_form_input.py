import streamlit as st

import constants
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func

def execute(df_key, table_name, label_name, columns_names, item_key_column_name, item_key, default_values):
    def clear_state(modded):
        # intialize session state data obj
        st.session_state[constants.st_data_key] = {}
        # pre-fill sessions state data obj with any default values
        for column_name in columns_names:
            if column_name in default_values:
                st.session_state[constants.st_data_key][column_name] = default_values[column_name][constants.default_value]
            else:
                # just set as empty
                st.session_state[column_name] = ''
        st.session_state.modded = modded

    #constants
    if 'modded' not in st.session_state:
        clear_state(False)

    # initialize dataframe
    if df_key not in st.session_state:
        df = gsheets.load_or_create_the_table(table_name, columns_names)
        df_func.set_df(st=st, key=df_key, new_df=df)

    def remove_item(item, index):
        df = df_func.get_df(st, df_key)
        #Remove item from list in data table
        new_df = df_func.remove_col(df, index)
        df_func.set_df(st, df_key, new_df)
        st.session_state.modded = True
        # set_df(st, df_func.remove_col(df_func.get_df(st, df_key), index))

    def update_text(column_name):
        text_input = st.session_state[column_name]
        st.session_state[constants.st_data_key][column_name] = text_input

    def add_items():
        data = st.session_state[constants.st_data_key]
        df = df_func.get_df(st, df_key)
        name = data[constants.workers_name]
        # check if name already in table
        if not df[constants.workers_name].astype("object").str.contains(name).any():
            #update datatable
            df = df_func.add_row(df, data)
            df_func.set_df(st, df_key, df)
            clear_state(True)

    index = 0
    df = df_func.get_df(st, df_key)

    if item_key_column_name in df:
        for item in df[item_key_column_name]:
            index = index + 1
            st.checkbox(item, key="id_{}".format(item),  on_change=remove_item, args=(item, index, ))

    for column_name in columns_names:
        if not (column_name in default_values
                and not default_values[column_name][constants.is_display_column]):
            st.text_input(label=column_name, value=st.session_state[column_name], on_change=update_text, key=column_name, args=(column_name,))

    st.button(label="add {}".format(table_name), on_click=add_items)

    def done():
        # update sheet
        gsheets.create_of_update_the_table(df_func.get_df(st, df_key), table_name)
        st.session_state.modded = False

    st.button("commit to db", on_click=done, disabled=(not st.session_state.modded))