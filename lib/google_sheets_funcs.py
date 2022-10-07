import streamlit as st
from pandas import DataFrame
from google.oauth2 import service_account
from gspread_pandas import Spread,Client

import lib.util as util
from lib import df_funcs as df_func
import constants
import traceback

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

xls_name = "initial you are interesting"

cache_time = 10

# Functions
# @st.cache(ttl = cache_time)
# Get our worksheet names
def get_worksheet_names(worksheet_list):
    sheet_names = []
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)
    return sheet_names


# @st.cache(allow_output_mutation=True)
def get_spread(credentials):
    client = Client(scope=scope,creds=credentials)
    spread = Spread(xls_name, client = client)
    sh = client.open(xls_name)
    return spread, client, sh

# @st.cache(ttl = cache_time)
def get_worksheets(sh):
    # Check whether the sheets exists
    return sh.worksheets()


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes = scope)

spread, client, sh = get_spread(credentials)

def createDataframe(columns):
    df = DataFrame(columns = columns)
    # index = columns[0]
    # df.set_index(index)
    return df

# @st.cache(ttl = cache_time)
def get_worksheet_list():
    return get_worksheets(sh)

# @st.cache(ttl = cache_time)
def get_worksheet(name):
    return get_worksheet_list()[name]

# Get the sheet as dataframe
# @st.cache(allow_output_mutation=True, ttl = cache_time)
def load_table(st, table_name, df_key_name, createTable=False, columns=None):
    try:
        worksheet = sh.worksheet(table_name)
        df = spread.sheet_to_df(index=0, sheet=worksheet)
    except Exception as e:
        print("Exception thrown")
        print(e)
        tb = traceback.format_exc()
        print(tb)
        if createTable:
            # create the dataframe for the table
            df = createDataframe(columns=columns)
            # create the table
            df = create_or_update_the_table(dataframe=df, table_name=table_name)
            worksheet = sh.worksheet(table_name)
        else:
            raise e

    # cache the df
    util.set_session_state_value(st=st, key=df_key_name, value=df)
    # stash specific worksheet in cache, create the worksheet obj if not exist
    worksheets = util.get_session_state_value(st=st, key=constants.worksheets_df_key, initValue={})
    worksheets[df_key_name] = worksheet
    util.set_session_state_value(st=st, key=constants.worksheets_df_key, value=worksheets)
    return df

# Update to Sheet
def create_or_update_the_table(dataframe, table_name):
    spread.df_to_sheet(dataframe, sheet = table_name, replace = True, index = False)
    # st.sidebar.info('Updated to GoogleSheet')
    return dataframe

def update_cell(worksheet, row, column, value):
    worksheet.update_cell(row, column, value)

def append_row(worksheet, values):
    worksheet.append_row(values)

def update_cells(worksheet, row, columns, values):
    str = None
    for column in columns:
        column_name = util.get_column_google_name(column)
        if not str:
            str = "{}{}".format(column_name, row)
        else:
            str = str + ":" + "{}{}".format(column_name,row)
    print(str)
    worksheet.update(str, values)

def insert_row(worksheet, column_values):
    worksheet.append_row(column_values)

def reload_table(st, table_name, df_key):
    worksheet = sh.worksheet(table_name)
    df = spread.sheet_to_df(index=0, sheet=worksheet)
    util.set_session_state_value(st, df_key, df)
