from pandas import DataFrame

def remove_row(df, index):
    return df.drop(df.index[index - 1]).reset_index(drop=True)

def add_row(df, row_data):
    if len(df.index) > 0:
        df.loc[len(df.index)]=row_data
    else:
        df.loc[0] = row_data
    return df.reset_index(drop=True)
