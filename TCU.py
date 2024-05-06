import numpy as np
import pandas as pd

def tcu(lst):

    df = pd.Series(lst)

    cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100  # Coeficiente de variação
    while cv(df) >= 25:
        mean = df.mean()
        std = df.std()
        df = df[(df > mean - std) & (df < mean + std)]
    return df.mean()