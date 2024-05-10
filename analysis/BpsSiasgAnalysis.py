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

def bpsSiasgAnalysis():

    path_root = Path(__file__).parents[1]
    sys.path.append(str(path_root))

    dict = {
        "BPS": np.nan,
        "TCU": np.nan,
        "TCE": np.nan,
        "AIQ": np.nan,
        "Chauvenet": np.nan
    }

    filePath = input("Digite o caminho para o arquivo: ")

    df = pd.read_csv(filePath, delimiter=";", skiprows=2, encoding='latin1')
    df['Preço Unitário'] = DOTANDCOMMA.dotAndComma(df['Preço Unitário']).astype(float)

    dict['BPS'] = BPS.bps(df['Preço Unitário'].tolist())
    dict['TCU'] = TCU.tcu(df['Preço Unitário'].tolist())
    dict['TCE'] = TCE.tce(df['Preço Unitário'].tolist())
    dict['AIQ'] = IQR.AIQ(df['Preço Unitário'])
    dict['Chauvenet'] = CHAUVENET.chauvenet(df['Preço Unitário'])
        
    return dict