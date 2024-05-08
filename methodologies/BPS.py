import pandas as pd

def bps(lst):
    # Transforma a lista em uma Series do pandas
    series = pd.Series(lst)
    
    # Calcula a média e o desvio padrão da Series
    media = series.mean()
    desvio_padrao = series.std()
    
    # Calcula os valores de y e z conforme especificado
    y = media - desvio_padrao
    z = media + desvio_padrao
    
    # Filtra os elementos da Series que satisfazem a condição x >= y ou x <= z
    elementos_condicionais = series[(series >= y) & (series <= z)]
    
    return elementos_condicionais.mean()
