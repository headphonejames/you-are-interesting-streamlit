from pandas import DataFrame

def set_session_state_value(st, key, value):
    st.session_state[key] = value

def get_session_state_value(st, key):
    return st.session_state[key]


def remove_col(df, index):
    return df.drop(df.index[index - 1]).reset_index(drop=True)

def add_row(df, row_data):
    if len(df.index) > 0:
        df.loc[len(df.index)]=row_data
    else:
        df.loc[0] = row_data
    return df.reset_index(drop=True)
