from pandas import DataFrame

def set_df(st, new_df):
    st.session_state.dataframe = new_df

def get_df(st):
    return st.session_state.dataframe


def remove_col(df, index):
    return df.drop(df.index[index - 1]).reset_index(drop=True)

def add_col(df, col_data):
    if len(df.index) > 0:
        df.loc[len(df.index)]=col_data
    else:
        df.loc[0] = col_data
    return df.reset_index(drop=True)
