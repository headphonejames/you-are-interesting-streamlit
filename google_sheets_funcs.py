import streamlit as st
from pandas import DataFrame
from google.oauth2 import service_account
from gspread_pandas import Spread,Client

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

spreadsheetname = "initial you are interesting"

# Functions
@st.cache()
# Get our worksheet names
def get_worksheet_names(worksheet_list):
    sheet_names = []
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)
    return sheet_names

# Get the sheet as dataframe
@st.cache()
def load_the_spreadsheet(sh, spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
@st.cache()
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Compound CID','Time_stamp']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

@st.cache(allow_output_mutation=True)
def get_spread(credentials):
    client = Client(scope=scope,creds=credentials)
    spread = Spread(spreadsheetname,client = client)
    sh = client.open(spreadsheetname)
    return spread, client, sh

@st.cache()
def get_worksheets(sh):
    # Check whether the sheets exists
    return sh.worksheets()


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes = scope)

spread, client, sh = get_spread(credentials)

def get_worksheet_list():
    return get_worksheets(sh)

