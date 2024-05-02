import pandas as pd
import re

def weighted_average (values, quantities):
    result = 0
    for i in range(len(values)):
        result += float(values[i])*quantities[i]
    return result/sum(quantities);

def is_positive_integer(user_input):
    if re.match(r'^[1-9]\d*$', user_input):
        return True
    else:
        return False

while(True):

    filesNumber = input("Quantos arquivos Excel (.xlsx) você deseja enviar?")

    if(is_positive_integer(filesNumber)):
        filePath = input("Digite o caminho para o arquivo 1:")
        df = pd.read_excel(filePath, skiprows=4)
        for i in range(1, filesNumber):
            filePath = input("Digite o caminho para o arquivo "+(i+1)+":")
            df = pd.read_excel(filePath, skiprows=4)
        
        pd.set_option('display.max_columns', None)
        print(df)
        break
    else:
        print("Número inválido de arquivos. Digite novamente.")
#print(weighted_average(list(map(lambda x: x.replace(',', '.'), df['Valor Unitário'].tolist())), df['Quantidade Ofertada'].tolist()))