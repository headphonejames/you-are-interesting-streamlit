import streamlit as st
import constants
import util
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func

def start_shift(worker_name, index):
    workers_df = df_func.get_session_state_value(st, constants.workers_dataframe_key_name)
    worksheet = df_func.get_session_state_value(st, constants.worksheet_key)
    # update "isworking" value
    workers_df.at[index,constants.worker_is_working]= True
    # update just those cells in the worksheet
    column_index = workers_df.columns.get_loc(constants.worker_is_working) + 1
    # index add 2 (starts at 1, +1  for headers)
    gsheets.update_cell(worksheet=worksheet,
                        row=index+2,
                        column=column_index,
                        value=True)
    df_func.set_session_state_value(st, constants.workers_dataframe_key_name, workers_df)
    # go to waiting_for_friend

def execute():
    # initialize dataframe
    if constants.workers_dataframe_key_name not in st.session_state:
        gsheets.load_or_create_the_table(constants.workers_table_name,
                                         constants.workers_dataframe_key_name,
                                         constants.workers_config_columns_names)

    df = df_func.get_session_state_value(st, constants.workers_dataframe_key_name)

    for index, row in df.iterrows():
        worker_name = row[constants.workers_name]
        is_working =  util.convert_to_boolean(row[constants.worker_is_working])
        if not is_working:
            st.button(worker_name, key="id_{}".format(worker_name),
                      on_click = start_shift,
                      args=(worker_name, index, ))

    st.button("back to main", on_click=util.update_current_page, kwargs={"page": constants.ENRTY})