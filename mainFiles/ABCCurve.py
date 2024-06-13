import pandas as pd
import numpy as np
import os
from utilities.dotAndComma import dotAndComma
from utilities.dotAndComma import dot
from utilities.real import real

def ABCCurve(filePath, pasta_criada):
    df = pd.read_excel(filePath)

    print("Arquivo em excel contendo apenas a tabela na seguinte ordem\n[ITEM] [DISCRIMINAÇÃO] [UNIDADE] [QUANTIDADE] [VALOR UNITÁRIO] [VALOR TOTAL] [PARTICIPAÇÃO]")
    maxNum = len(df)-1
    ind = np.arange(1, maxNum+1, 1)
    df[df.columns[3]] = dot(df[df.columns[3]]) #tratamento do "."
    df[df.columns[4]] = real(df[df.columns[4]]) #tratamento do "R$"
    df[df.columns[5]] = real(df[df.columns[5]]) #tratamento do "R$"
    df.insert(6,'VTC', dotAndComma(df[df.columns[3]]) * dotAndComma(df[df.columns[4]]))
    df.insert(7,'PERCENTUAL', df['VTC'] / sum(df['VTC']) * 100)
    df['PERCENTUAL'] = df['PERCENTUAL'].round(2)

    ABC_curve = df.sort_values(by='VTC', ascending=False)
    ABC_curve = ABC_curve.reset_index(drop=True)

    ABC_curve.index = ABC_curve.index + 1
    ABC_curve.index.name = "ABC"

    ABC_curve["MÉDIA BPS"] = np.nan
    ABC_curve["MÉDIA TCU"] = np.nan
    ABC_curve["MÉDIA TCE"] = np.nan
    ABC_curve["MÉDIA AIQ"] = np.nan
    ABC_curve["MÉDIA CHAUVENET"] = np.nan

    ABC_curve["% MÉDIA BPS"] = np.nan
    ABC_curve["% MÉDIA TCU"] = np.nan
    ABC_curve["% MÉDIA TCE"] = np.nan
    ABC_curve["% MÉDIA AIQ"] = np.nan
    ABC_curve["% MÉDIA CHAUVENET"] = np.nan
    ABC_curve["OBSERVAÇÕES"] = "Adicionar"

    # ABC_curve["ANÁLISE BPS"] = np.nan
    # ABC_curve["ANÁLISE TCU"] = np.nan
    # ABC_curve["ANÁLISE TCE"] = np.nan
    # ABC_curve["ANÁLISE AIQ"] = np.nan 
    # ABC_curve["ANÁLISE CHAUVENET"] = np.nan

  

    caminho_novo_arquivo = os.path.join(pasta_criada, 'Análise Completa.xlsx')
    print(caminho_novo_arquivo)
    ABC_curve.to_excel(caminho_novo_arquivo)
    return caminho_novo_arquivo