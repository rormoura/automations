import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

def cleanData(lista_dicionarios):
    
    df = pd.DataFrame(lista_dicionarios)
    df = df[df['precoUnitario'] != 0]
    df = df.drop_duplicates(subset='idCompra', keep='first')
    df['dataCompra'] = pd.to_datetime(df['dataCompra'])
    data_limite = datetime.now(pytz.UTC) - timedelta(days=11*30)
    df = df[df['dataCompra'] >= data_limite]
    df['dataCompra'] = df['dataCompra'].dt.tz_convert('America/Sao_Paulo')
    df['dataCompra'] = df['dataCompra'].dt.strftime('%d/%m/%Y %H:%M:%S')
    df = df.sort_values(by='precoUnitario')
    df['Unidade'] = df[['nomeUnidadeFornecimento', 'capacidadeUnidadeFornecimento', 'siglaUnidadeMedida']].apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

    return df