import pandas as pd

def real (df):
    if(df.dtype == object):
        elements = []
        for x in df:
            x = str(x)
            if('R$' in x):
                x = x.replace('R$', '')
            if(' ' in x):
                x = x.replace(' ', '')
            elements.append(x)
        return pd.Series(elements)
    return df