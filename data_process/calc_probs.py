import pandas as pd
import numpy as np

df = pd.read_csv('supermarket_df_final.csv', sep=';', parse_dates=['timestamp'])
P = pd.crosstab(
    df['location'], 
    df['location_next'],
    normalize='index')

P['entrance_temp'] = 0
P.insert(3, 'entrance', P['entrance_temp'])
P.drop(columns=['entrance_temp'], inplace=True)

PROBS = P.to_dict(orient='index')
for key in PROBS.keys():
    PROBS[key] = list(PROBS[key].values())

