import pandas as pd
import re

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

import methodologies.TCE as TCE

def weighted_average (values, quantities):
    result = 0
    for i in range(len(values)):
        result += float(values[i])*quantities[i]
    return result/sum(quantities)

def is_positive_integer(user_input):
    if re.match(r'^[1-9]\d*$', user_input):
        return True
    else:
        return False



filesNumber = input("Quantos arquivos Excel (.xlsx) você deseja enviar?")

if(is_positive_integer(filesNumber)):
    dfs = []
    for i in range(int(filesNumber)):
        filePath = input("Digite o caminho para o arquivo "+str(i+1)+":")
        df = pd.read_excel(filePath, skiprows=4, converters={'Quantidade Ofertada': str})
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_excel("C:/Users/rormo/Downloads/relatorio_painel_concat.xlsx")
    print("TCE: "+str(TCE.tce(list(map(lambda x: float(x.replace(',', '.')), combined_df['Valor Unitário'].tolist())))))
    print("Média ponderada: "+str(weighted_average(list(map(lambda x: x.replace(',', '.'), combined_df['Valor Unitário'].tolist())), list(map(lambda x: int(x.replace('.', '')) if ("." in x) else int(x), combined_df['Quantidade Ofertada'])))))
else:
    print("Número inválido de arquivos. Digite novamente.")