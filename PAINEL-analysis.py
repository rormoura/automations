import pandas as pd

def weighted_average (values, quantities):
    result = 0
    for i in range(len(values)):
        result += float(values[i])*quantities[i]
    return result/sum(quantities);

filePath = "C:/Users/rormo/Downloads/painel_precos.csv"

df = pd.read_csv(filePath, delimiter=";", skiprows=1, encoding='latin1')
pd.set_option('display.max_columns', None)
print(df)
#print(weighted_average(list(map(lambda x: x.replace(',', '.'), df['Preço Unitário'].tolist())), df['Qtd Itens Comprados'].tolist()))