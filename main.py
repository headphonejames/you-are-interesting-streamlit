import streamlit as st

if 'workers' not in st.session_state:
    st.session_state.workers = ['james', 'not james']

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

