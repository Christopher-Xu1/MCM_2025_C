import pandas as pd


df = pd.read_csv('../Data/sports_codes.csv')
rows = df.shape[0]

for index, row in df.iterrows():

    print('"' +row['Code'] + '"' + ',')
