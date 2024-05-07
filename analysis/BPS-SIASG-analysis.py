import pandas as pd

def weighted_average (values, quantities):
    result = 0
    for i in range(len(values)):
        result += float(values[i])*quantities[i]
    return result/sum(quantities);

filePath = "C:/Users/rormo/Downloads/Geral_SIASG.csv"

df = pd.read_csv(filePath, delimiter=";", skiprows=2, encoding='latin1')

print(weighted_average(list(map(lambda x: x.replace(',', '.'), df[df.columns[19]].tolist())), df[df.columns[18]].tolist()))