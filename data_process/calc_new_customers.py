import pandas as pd

# read file processed by data_cleaning.py
df = pd.read_csv('supermarket_df_final.csv', sep=';', parse_dates=True, index_col=None)

# get entertime of every customer
df_entertime = df.groupby('customer_no').first()

# groupby timestamp and get each new customer amount
df_entertime = df_entertime.groupby('timestamp').count()
df_entertime.drop(['spend_time', 'location_next'],axis=1, inplace=True)
df_entertime.rename(columns={'location':'amount'}, inplace=True)

NEW_MEAN = df_entertime['amount'].mean()
NEW_STDDEV = df_entertime['amount'].std()