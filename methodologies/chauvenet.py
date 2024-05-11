import pandas as pd
import numpy as np
from scipy.stats import norm

def chauvenet(df):

        df = df.to_frame()
        cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100
        
        breakValue = df[df.columns[0]].mean()
 
        while ((cv(df[df.columns[0]]) > 25)) :

            mean = df[df.columns[0]].mean()
            std_dev = df[df.columns[0]].std()
            normValue = norm.ppf(1-1/(4*len(df[df.columns[0]])))

            minValue = (mean - (normValue * std_dev))
            maxValue = mean + (normValue*std_dev)

            df = df[df[df.columns[0]] >= minValue]
            df = df[df[df.columns[0]] <= maxValue]

            if (breakValue == df[df.columns[0]].mean()):
                break
            breakValue = df[df.columns[0]].mean()

        return df[df.columns[0]].mean()
