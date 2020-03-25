import numpy as np
import pandas as pd
from IPython.display import display


def display_all(df):
    """ Set max rows and columns to display """
    with pd.option_context("display.max_rows",1000):
        with pd.option_context("display.max_columns",1000):
            display(df)

def drop_missing_data(df,threshold=0.5,drop_cols=[]):
    """Process missing columns"""
    if not drop_cols:
        rows = len(df)
        num_nonna = round((1-threshold) * rows,0)
        for k,v in (df.isnull().sum()/rows).items():
            if v>threshold:
                drop_cols.append(k)
        
        d= df.dropna(axis=1,thresh = num_nonna)
    else:
        d= df.drop(drop_cols,axis=1)
            
    
    return d,drop_cols


def processing_date(df,col,attr=["year","month","day"],drop=True):
    """Process datatime column"""
    if not np.issubdtype(df[col],np.datetime64):
        df[col] = pd.to_datetime(df[col],infer_datetime_format=True)
    
    for ea in attr:
        df[col+"_"+ea] = getattr(df[col].dt,ea)
    
    if drop:
        df.drop(col,axis=1, inplace=True)


def fill_numeric(df,missing_val):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col].dtypes):
            if df[col].isnull().sum():
                df[col].fillna(df[col].median(),inplace=True)
                missing_val[col] = df[col].median()
    return missing_val

def processing_missing(df,missing_val={}):
    """Process missing values"""
    s= df.copy()
    if not missing_val:
        missing_val = fill_numeric(s,missing_val)
    
    else:
        for k,v in missing_val.items():
            if s[k].isnull().sum():
                s[k].fillna(v,inplace=True)
        
        if d.isnull().sum().sum():
            for col in s.columns:
                missing_val = fill_numeric(s,missing_val)

    return s,missing_val


def convert_category(df,cat_cols=[]):
    if cat_cols:
        for col in cat_cols:
                df[col] = df[col].astype("category")
    else:
        obj_columns = df.select_dtypes(['object']).columns
        for obj in obj_columns:
            df[obj] = df[obj].astype('category')
            cat_cols.append(obj)
    return df, cat_cols



def set_catagory(df,cat_dict={}):
    if cat_dict:
        for k,v in cat_dict.items():
            df[k] = df[k].cat.set_categories(v)
    else:
        for col in df.columns:
            if df[col].dtypes.name =="category":
                cat_dict[col] = df[col].cat.categories
    return cat_dict

def generate_dummies(df,cat_cols,max_cardi):
    cardi_cols = []
    for col in cat_cols:
        if len(df[col].cat.categories) <= max_cardi:
            cardi_cols.append(col)
    
    df = pd.get_dummies(df,columns = cardi_cols,prefix=cardi_cols,drop_first=True)
    
    return df, cardi_cols


def category_codes(df,cat_cols):
    for col in cat_cols:
        df[col] = df[col].cat.codes+1
    

def proc_category(df,cat_cols=[],cat_dict={},max_cardi=None):
    """Process categorical variables """
    d = df.copy()
    
    d, cat_cols = convert_category(d,cat_cols)

    cat_dict = set_catagory(d,cat_dict)
    
    if max_cardi:
        d,cardi_cols = gen_dummies(d,cat_cols,max_cardi)
        cat_cols = list(set(cat_cols) - set(cardi_cols))
    
    cat_codes(d,cat_cols)
    
    return d, cat_dict

def split_train_test(df,num_test,shuffle=False):
    """
    Split df into training and tes set"""
    if shuffle:
        df = df.sample(frac=1).reset_index(drop=True)
    
    n_trn = len(df) - num_test
    n_train = df[:n_trn]
    n_test = df[n_trn:]
    
    return n_train, n_test
