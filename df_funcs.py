from pandas import DataFrame

def remove_col(df, index):
    return df.drop(df.index[index - 1])

def add_col(df, col_data):
    df.loc[len(df)]=col_data
    return df
