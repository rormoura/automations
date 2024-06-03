import pandas as pd

def dotAndComma (df):
    if(df.dtype == object):
        elements = []
        for x in df:
            x = str(x)
            if(',' in x):
                x = x.replace(',', '.')
            elements.append(float(x))
        return pd.Series(elements)
    return df

def dot (df):
    if(df.dtype == object):
        elements = []
        for x in df:
            x = str(x)
            if('.' in x):
                x = x.replace('.', '')
            elements.append(float(x))
        return pd.Series(elements)
    return df