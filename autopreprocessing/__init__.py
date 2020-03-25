import numpy as np
import pandas as pd
from IPython.display import display
from pandas import read_csv, get_dummies, Series
from numpy import nan, zeros

def display(df):
    """Set max rows and columns to display"""
    with pd.option_context("display.max_rows",1000):
        with pd.option_context("display.max_columns",1000):
            display(df)

def load_csv(filePath, missing_headers=False):
    """Read data as csv and return as pandas data frame."""

    if missing_headers:
        data = read_csv(filePath, header=None)
    else:
        data = read_csv(filePath, header=0)

    # make shape of data frame global
    global rows, cols
    rows, cols = data.shape

    return data

def replace_missing_data(data):
    """replace missing data values and return as pandas data frame."""

    # strip whitespace from data
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # replace missing values with the sentinel NaN value
    data = data.replace('?', nan)

    data = data.replace('nan', 0)

    # get missing field count
    nan_vals = dict(data.count(axis=1))
    nan_vals = {key: value for (key, value) in nan_vals.items() if value < cols-2}

    # remove samples with more than one missing field
    data = data.drop(index=nan_vals.keys())

    return data

def drop_missing_data(df,threshold=0.5,drop_cols=[]):
    """Process missing columns"""
    if not drop_cols:
        rows = len(df)
        num_nonna = round((1-threshold) * rows,0)
        for i,s in (df.isnull().sum()/rows).items():
            if s>threshold:
                drop_cols.append(i)

        data= df.dropna(axis=1,thresh = num_nonna)
    else:
        data= df.drop(drop_cols,axis=1)


    return data,drop_cols
def processing_date(df,col,attr=["year","month","day"],drop=True):
    """Process datatime columns"""
    if not np.issubdtype(df[col],np.datetime64):
        df[col] = pd.to_datetime(df[col],infer_datetime_format=True)

    for s in attr:
        df[col+"_"+s] = getattr(df[col].dt,s)

    if drop:
        df.drop(col,axis=1, inplace=True)


def one_hot_encode(data):
    """Perform a one-hot encoding and return as pandas data frame."""
    return get_dummies(data)

def split_data(df,num_test,shuffle=False):
    """Split df into training and validation set"""
    if shuffle:
        df = df.sample(frac=1).reset_index(drop=True)
    n_trn = len(df) - num_test
    n_train = df[:n_trn]
    n_test = df[n_trn:]
    return n_train, n_test
