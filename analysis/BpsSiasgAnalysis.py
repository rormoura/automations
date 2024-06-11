import pandas as pd
import numpy as np

from pathlib import Path
import sys

import methodologies.BPS as BPS
import methodologies.TCE as TCE
import methodologies.TCU as TCU
import methodologies.IQR as IQR
import methodologies.chauvenet as CHAUVENET
import utilities.dotAndComma as DOTANDCOMMA

import difflib

def mostrar_diferencas(string1, string2):
    diff = difflib.ndiff(string1, string2)
    print('\n'.join(diff))

def bpsSiasgAnalysis(filePath):

    path_root = Path(__file__).parents[1]
    sys.path.append(str(path_root))

    dict = {
        "BPS": np.nan,
        "TCU": np.nan,
        "TCE": np.nan,
        "AIQ": np.nan,
        "Chauvenet": np.nan
    }

    data_frame_verify = pd.read_csv(filePath, delimiter=";", encoding='latin1')
    expectated_value = "  Base de dados SIASG"
    if(data_frame_verify.columns[0][2:] != expectated_value[2:]):
        return -1

    df = pd.read_csv(filePath, delimiter=";", skiprows=2, encoding='latin1')
    df['Preço Unitário'] = DOTANDCOMMA.dotAndComma(df['Preço Unitário']).astype(float)
    df = df.sort_values(by=['Preço Unitário'], ascending=True)

    dict['BPS'] = BPS.bps(df['Preço Unitário'].tolist())
    dict['TCU'] = TCU.tcu(df['Preço Unitário'].tolist())
    dict['TCE'] = TCE.tce(df['Preço Unitário'].tolist())
    dict['AIQ'] = IQR.AIQ(df['Preço Unitário'])
    dict['Chauvenet'] = CHAUVENET.chauvenet(df['Preço Unitário'])
        
    return dict