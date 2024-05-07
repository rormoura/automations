import pandas as pd

def tce(lst):

    df = pd.Series(lst)

    Q1 = 0.25*df.count()
    Q4 = 0.75*df.count()

    # Remove os valores que estão no primeiro e no quarto quartil
    df = df[((df.index)+1 >= Q1) & ((df.index)+1 <= Q4)]

    # Retorna a média dos valores restantes
    return df.mean()