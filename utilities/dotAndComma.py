#This function receives a dataframe column and returns a dataframe column.
#It takes each line, which is a number, from the column and:
#   1 - If there is a dot, it removes the dot.
#   2 - If there is a comma, it replaces the comma with a dot.

def dotAndComma (df):
    if(df.dtype == object):
        df = df.apply(lambda x: float(x.replace('.', '')) if ('.' in x) else x)
        df = df.apply(lambda x: float(x.replace(',', '.')) if (',' in x) else x)
    return df