import pandas as pd
import numpy as np
from scipy.stats import norm

def chauvenet(df):
        df = df.to_frame()
        cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100
        while (cv(df[df.columns[0]]) > 25):
                mean = df[df.columns[0]].mean()
                std_dev = df[df.columns[0]].std()
                df['distancia'] = np.abs(df[df.columns[0]] - mean) / std_dev
                df['probabilidade'] = 1 - norm.cdf(df['distancia'])
                N = len(df[df.columns[0]])
                limite_chauvenet = 0.5 / N
                df = df[df['probabilidade'] >= limite_chauvenet]
        
        return df[df.columns[0]].mean()
