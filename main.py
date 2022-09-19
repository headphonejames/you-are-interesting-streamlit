import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")


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

