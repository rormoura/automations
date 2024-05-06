import numpy as np
import pandas as pd
from scipy.stats import iqr


def AIQ (data):
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = (Q3 - Q1)

        data2 = data[(data > Q1 -(1.5* IQR)) & (data < Q3 +(1.5* IQR))]
        return(data2.mean())