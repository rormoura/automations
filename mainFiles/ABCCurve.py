import pandas as pd
import numpy as np
from utilities.dotAndComma import dotAndComma

def ABCCurve(filePath):
    excelRaw = pd.read_excel(filePath)

    print("Arquivo em excel contendo apenas a tabela na seguinte ordem\n[ITEM] [DISCRIMINAÇÃO] [UNIDADE] [QUANTIDADE] [VALOR UNITÁRIO] [VALOR TOTAL] [PARTICIPAÇÃO]")
    maxNum = len(excelRaw)-1

    df = excelRaw
    ind = np.arange(1, maxNum+1, 1)

    df.insert(6,'VTC', dotAndComma(df[df.columns[3]]) * dotAndComma(df[df.columns[4]]))
    df.insert(7,'PERCENTUAL', df['VTC'] / sum(df['VTC']) * 100)

    ABC_curve = df.sort_values(by='PERCENTUAL', ascending=False)
    ABC_curve = ABC_curve.reset_index(drop=True)

    ABC_curve.index = ABC_curve.index + 1
    ABC_curve.index.name = "ABC"

    ABC_curve.to_excel('curvaABC.xlsx')
    ABC_curve.to_csv('curvaABC.csv')