import streamlit as st
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func

def execute(df_key, table_name, label_name, columns_names, item_key_column_name, item_key):
    #constants
    if 'modded' not in st.session_state:
        st.session_state.modded = False
        st.session_state["data"] = {}

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

    def clear_state(df):
        df_func.set_df(st, df_key, df)
        for column_name in columns_names:
            st.session_state[column_name] = ''
        st.session_state.modded = True

    def update_text(column_name):
        text_input = st.session_state[column_name]
        st.session_state["data"][column_name] = text_input

    def add_items():
        data = st.session_state["data"]
        df = df_func.get_df(st, df_key)
        item_key_data = data[columns_names[0]]
        # check if items already exists
        if not item_key_data in df[columns_names[0]].tolist():
            #update datatable
            df = df_func.add_row(df, data)
            clear_state(df)

    index = 0
    df = df_func.get_df(st, df_key)

    if item_key_column_name in df:
        for item in df[item_key_column_name]:
            index = index + 1
            st.checkbox(item, key="id_{}".format(item),  on_change=remove_item, args=(item, index, ))

    for column_name in columns_names:
        st.text_input(label=column_name, on_change=update_text, key=column_name, args=(column_name,))

    st.button(label="add {}".format(table_name), on_click=add_items)

    def done():
        # update sheet
        gsheets.create_of_update_the_table(df_func.get_df(st, df_key), table_name)
        st.session_state.modded = False

    st.button("commit to db", on_click=done, disabled=(not st.session_state.modded))