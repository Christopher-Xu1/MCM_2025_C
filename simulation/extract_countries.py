import pandas as pd


df = pd.read_csv("../Data/summerOly_athletes.csv")


countries = {}
for index, row in df.iterrows():
    if row['NOC'] not in countries:
        countries[row['NOC']] = 1
    else:
        continue

for x in countries:
    print('"' + x +'"' + ',')