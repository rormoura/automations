import pandas as pd
import numpy as np

filePath ="C:/Users/mathe/OneDrive/Área de Trabalho/ESTÁGIO/curvaABC.xlsx" 
df = pd.read_excel(filePath,index_col=0)

df["MÉDIA BPS"] = np.nan
df["MÉDIA TCU"] = np.nan
df["MÉDIA TCE"] = np.nan
df["MÉDIA AIQ"] = np.nan
df["MÉDIA CHAUVENET"] = np.nan

df["DISTINTO EM RELAÇÃO À MÉDIA BPS"] = np.nan
df["DISTINTO EM RELAÇÃO À MÉDIA TCU"] = np.nan
df["DISTINTO EM RELAÇÃO À MÉDIA TCE"] = np.nan
df["DISTINTO EM RELAÇÃO À MÉDIA AIQ"] = np.nan
df["DISTINTO EM RELAÇÃO À MÉDIA CHAUVENET"] = np.nan

df["ANÁLISE EM RELAÇÃO AO BPS"] = np.nan
df["ANÁLISE EM RELAÇÃO AO TCU"] = np.nan
df["ANÁLISE EM RELAÇÃO AO TCE"] = np.nan
df["ANÁLISE EM RELAÇÃO AO AIQ"] = np.nan
df["ANÁLISE EM RELAÇÃO AO "] = np.nan

df["OBSERVAÇÕES"] = np.nan
print(list(df.columns.values))

