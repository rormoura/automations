import pandas as pd
import numpy as np

from pathlib import Path
import sys

import methodologies.TCE as TCE
import methodologies.TCU as TCU
import methodologies.IQR as IQR
import methodologies.chauvenet as CHAUVENET
import utilities.dotAndComma as DOTANDCOMMA

def panelAnalysis(filesPaths):
    path_root = Path(__file__).parents[1]
    sys.path.append(str(path_root))

    dict = {
        "BPS": np.nan,
        "TCU": np.nan,
        "TCE": np.nan,
        "AIQ": np.nan,
        "Chauvenet": np.nan
    }
    dfs = []
    for filePath in filesPaths:

        data_frame_verify = pd.read_excel(filePath, converters={'Quantidade Ofertada': str})
        expectated_value = "Tipo painel:"
        if(data_frame_verify.columns[0][2:] != expectated_value[2:]):
            return -1

        df = pd.read_excel(filePath, skiprows=4, converters={'Quantidade Ofertada': str})
        df['Quantidade Ofertada'] = df['Quantidade Ofertada'].apply(lambda x: x.replace('.', '') if ('.' in x) else x)
        df['Quantidade Ofertada'] = df['Quantidade Ofertada'].astype(float)
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['Valor Unitário'] = DOTANDCOMMA.dotAndComma(combined_df['Valor Unitário'])

    combined_df = combined_df.sort_values(by=['Valor Unitário'], ascending=True)
    dict['BPS'] = np.nan
    dict['TCU'] = TCU.tcu(combined_df['Valor Unitário'].tolist())
    dict['TCE'] = TCE.tce(combined_df['Valor Unitário'].tolist())
    dict['AIQ'] = IQR.AIQ(combined_df['Valor Unitário'])
    dict['Chauvenet'] = CHAUVENET.chauvenet(combined_df['Valor Unitário'])
    
    return dict