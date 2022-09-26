import streamlit as st
import google_sheets_funcs as gsheets
import df_funcs as df_func

#constants
worker_table_name = "workers"


def set_df(new_df):
    st.session_state.dataframe = new_df

def get_df():
    return st.session_state.dataframe

# initialize worker list
if 'workers' not in st.session_state:
    set_df(gsheets.load_the_table(worker_table_name))
    print(get_df())
    if (get_df().empty):
        workers = []
    else:
        workers = get_df()["workers"].values.tolist()
    st.session_state.workers = workers

#local vars
wlist = st.session_state.workers

def remove_worker(worker, index):
    #Remove worker from list in data table
    set_df(df_func.remove_col(get_df(), index-1))
    #Remove worker name from ui list
    wlist.remove(worker)
    # update sheet
    gsheets.update_the_table(get_df(), worker_table_name)

def add_worker():
    worker_name = st.session_state.worker_name
    if not worker_name in wlist:
        # add to ui list
        wlist.append(worker_name)
        #update datatable
        set_df(df_func.add_col(get_df(),  worker_name))
        # update sheet
        gsheets.update_the_table(get_df(), worker_table_name)
        # clear state
        st.session_state.worker_name = ''

st.title('Who is staffing?')

index = 0
for worker in wlist:
    index = index + 1
    st.checkbox(worker, key="id_{}".format(worker),  on_change=remove_worker, args=(worker, index, ))

col1, col2 = st.columns([1,1])

st.text_input(label="worker name", placeholder="worker name", on_change=add_worker, key='worker_name')
