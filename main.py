import streamlit as st
import google_sheets_funcs as gsheets
import df_funcs as df_func

#constants
worker_table_name = "workers"

if 'modded' not in st.session_state:
    st.session_state.modded = False

def set_df(new_df):
    st.session_state.dataframe = new_df

def get_df():
    return st.session_state.dataframe

# initialize worker list
if 'dataframe' not in st.session_state:
    set_df(gsheets.load_the_table(worker_table_name))

def remove_worker(worker, index):
    #Remove worker from list in data table
    asdf = df_func.remove_col(get_df(), index)
    set_df(asdf)
    st.session_state.modded = True
    # set_df(df_func.remove_col(get_df(), index))

def add_worker():
    worker_name = st.session_state.worker_name
    if not worker_name in get_df()["workers"]:
        #update datatable
        set_df(df_func.add_col(get_df(),  worker_name))
        # clear state
        st.session_state.worker_name = ''
        st.session_state.modded = True

st.title('Who is staffing?')

index = 0
for worker in get_df()["workers"]:
    index = index + 1
    st.checkbox(worker, key="id_{}".format(worker),  on_change=remove_worker, args=(worker, index, ))

col1, col2 = st.columns([1,1])

st.session_state.worker_name = ''
st.text_input(label="worker name", placeholder="worker name", on_change=add_worker, key='worker_name')

def done():
    # update sheet
    gsheets.update_the_table(get_df(), worker_table_name)
    st.session_state.modded = False

st.button("submit", on_click=done, disabled=not st.session_state.modded)
