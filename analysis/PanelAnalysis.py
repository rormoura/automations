import pandas as pd
import numpy as np
import re

from pathlib import Path
import sys

import methodologies.TCE as TCE
import methodologies.TCU as TCU
import methodologies.IQR as IQR
import methodologies.chauvenet as CHAUVENET
import utilities.dotAndComma as DOTANDCOMMA

def is_positive_integer(user_input):
    if re.match(r'^[1-9]\d*$', user_input):
        return True
    else:
        return False

def panelAnalysis():
    path_root = Path(__file__).parents[1]
    sys.path.append(str(path_root))

    dict = {
        "BPS": np.nan,
        "TCU": np.nan,
        "TCE": np.nan,
        "AIQ": np.nan,
        "Chauvenet": np.nan
    }

    filesNumber = input("Quantos arquivos Excel (.xlsx) você deseja enviar?")

    if(is_positive_integer(filesNumber)):
        dfs = []
        for i in range(int(filesNumber)):
            filePath = input("Digite o caminho para o arquivo "+str(i+1)+":")
            df = pd.read_excel(filePath, skiprows=4, converters={'Quantidade Ofertada': str})
            dfs.append(df)
        
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df['Valor Unitário'] = DOTANDCOMMA.dotAndComma(combined_df['Valor Unitário'])

        combined_df = combined_df.sort_values(by=['Valor Unitário'], ascending=True)
        combined_df.to_excel("C:/Users/rormo/Downloads/combined.xlsx")
        dict['BPS'] = np.nan
        dict['TCU'] = TCU.tcu(combined_df['Valor Unitário'].tolist())
        dict['TCE'] = TCE.tce(combined_df['Valor Unitário'].tolist())
        dict['AIQ'] = IQR.AIQ(combined_df['Valor Unitário'])
        dict['Chauvenet'] = CHAUVENET.chauvenet(combined_df['Valor Unitário'])
        
        return dict
    else:
        return filesNumber