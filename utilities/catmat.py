import pandas as pd
import re

def catmat (df):
    if(df.dtype == object):
        elements = []
        for x in df:
            x = x.replace('BR', '')
            if('.' in x):
                x = re.sub(r'\.\d+|\.', '', x)
            if('/' in x):
                x = re.sub(r'\/\d+|\/', '', x)
            if('-' in x):
                x = re.sub(r'\-\d+|\-', '', x)
            elements.append(x)
        return pd.Series(elements, dtype=str)
    return df