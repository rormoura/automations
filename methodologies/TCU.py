import numpy as np
import pandas as pd

def tcu(lst):

    df = pd.Series(lst)

    mean = df.mean() #aplciando a limpeza uma vez antes do while
    std = df.std()
    df = df[(df >= (mean - std)) & (df <= (mean + std))]

    cv = lambda x: (np.std(x) / np.mean(x)) * 100  #Coeficiente de variação

    while cv(df) > 25:
        mean = df.mean()
        std = df.std()
        df = df[(df >= (mean - std)) & (df <= (mean + std))]
    return df.mean()