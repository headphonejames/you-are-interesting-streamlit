import streamlit as st
import google_sheets_funcs as gsheets

st.write(gsheets.get_worksheet_list())

what_sheets = gsheets.get_worksheet_names(gsheets.get_worksheet_list())
print(what_sheets)
#st.sidebar.write(what_sheets)
ws_choice = st.sidebar.radio('Available worksheets',what_sheets)

# initialize worker list
if 'workers' not in st.session_state:
    workers = ['james']
    st.session_state.workers = workers

wlist = st.session_state.workers

def remove_worker(worker):
    wlist.remove(worker)

def add_worker():
    worker = st.session_state.worker_name
    if not worker in wlist:
        wlist.append(worker)
        st.session_state.worker_name = ''

st.title('Who is staffing?')

for worker in wlist:
    st.checkbox(worker, key="id_{}".format(worker),  on_change=remove_worker, args=(worker, ))

col1, col2 = st.columns([1,1])

st.text_input(label="worker name", placeholder="worker name", on_change=add_worker, key='worker_name')

