import streamlit as st
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func

def execute(df_key, table_name, label_name, column_name, item_name, item_key):
    #constants
    if 'modded' not in st.session_state:
        st.session_state.modded = False

    # initialize dataframe
    if df_key not in st.session_state:
        df_func.set_df(st, df_key, gsheets.load_the_table(table_name))

    # initialize list of items
    if not column_name in df_func.get_df(st, df_key):
        # add item column to datatable
        updated_df = df_func.get_df(st, df_key)[column_name] = []
        df_func.set_df(st, df_key, updated_df)


    def remove_item(question, index):
        df = df_func.get_df(st, df_key)
        #Remove question from list in data table
        new_df = df_func.remove_col(df, index)
        df_func.set_df(st, df_key, new_df)
        st.session_state.modded = True
        # set_df(st, df_func.remove_col(df_func.get_df(st, df_key), index))

    def clear_state(df):
        df_func.set_df(st, df_key, df)
        st.session_state[item_key] = ''
        st.session_state.modded = True

    def add_item():
        df = df_func.get_df(st, df_key)
        item = st.session_state[item_key]
        # check if questions already exists
        if not item in df[column_name].tolist():
            #update datatable
            df = df_func.add_col(df, [item])
            clear_state(df)

    index = 0
    df = df_func.get_df(st, df_key)

    if item_name in df:
        for item in df[item_name]:
            index = index + 1
            st.checkbox(item, key="id_{}".format(item),  on_change=remove_item, args=(item, index, ))

    st.session_state.question_name = ''
    st.text_input(label='', placeholder=label_name, on_change=add_item, key=item_key)

    def done():
        # update sheet
        gsheets.update_the_table(df_func.get_df(st, df_key), table_name)
        st.session_state.modded = False

    st.button("commit to db", on_click=done, disabled=(not st.session_state.modded))