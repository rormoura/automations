import pandas as pd
from datetime import datetime, timedelta
import pytz

def cleanData(lista_dicionarios):
    
    df = pd.DataFrame(lista_dicionarios)
    df['dataCompra'] = pd.to_datetime(df['dataCompra'], format='ISO8601')
    df = df[df['precoUnitario'] != 0]
    data_limite = datetime.now(pytz.UTC) - timedelta(days=11*30)
    df = df[df['dataCompra'] >= data_limite]
    df = df.sort_values(by='precoUnitario')
    df = df.drop_duplicates(subset='idCompra', keep='first')
    
    return df