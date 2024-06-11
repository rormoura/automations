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

def bpsBpsAnalysis(filePath):

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
    expectated_value = "  Base de dados BPS"
    if(data_frame_verify.columns[0][2:] != expectated_value[2:]):
        return -1

    df = pd.read_csv(filePath, delimiter=";", skiprows=2, encoding='latin1')
    df[df.columns[18]] = DOTANDCOMMA.dotAndComma(df[df.columns[18]]).astype(float)
    df = df.sort_values(by=[df.columns[18]], ascending=True)

    dict['BPS'] = BPS.bps(df[df.columns[18]].tolist())
    dict['TCU'] = TCU.tcu(df[df.columns[18]].tolist())
    dict['TCE'] = TCE.tce(df[df.columns[18]].tolist())
    dict['AIQ'] = IQR.AIQ(df[df.columns[18]])
    dict['Chauvenet'] = CHAUVENET.chauvenet(df[df.columns[18]])
        
    return dict