# automations

#### This repo is dedicated to contain some python automations created by me and my friend @MatheusXimenesFerreira.

- Analysis folder contains codes related to "BPS" and "PAINEL DE PREÇOS" analysis.

- Main-Files folder contains codes related to create the main files of the price search: ABC Curve, Complete Analysis and Audit Report.

- Methodologies folder contains codes related to the following statistical methodologies: TCE, TCU, IQR and Chauvenet.

- Utilities folder contains useful codes related to formatting, organization and so on.

## Inside Analysis folder

> BpsBpsAnalysis.py: Receives a csv (.csv) file and returns a 5 element dictionary.

> BpsSiasgAnalysis.py: Receives a csv (.csv) file and returns a 5 element dictionary.

> PanelAnalysis.py: Receives an excel (.xlsx) file and returns a 5 element dictionary.

## Inside MainFiles folder

> ABCCurve.py: 

> AuditReport.py: 

> CompleteAnalysis.py: 

## Inside Methodologies folder

> BPS function: Receives a list of floats and returns a float number.

> TCE function: Receives a list of floats and returns a float number.

> TCU function: Receives a list of floats and returns a float number.

> IQR function: Receives a float pandas series and returns a float number.

> Chauvenet function: Receives a float pandas series and returns a float number.

## Inside Utilities folder

> dotAndComma function: Receives a dataframe column and returns a dataframe column. It assumes that there are no '.' for thousands separator, then replaces any ',' with '.'.