import pandas as pd

file_path = '../Data/processed_olympics_data/Australia_Baseball_mens.csv'

df = pd.read_csv(file_path)
rows = df.shape[0]


prev = ''
bronze_count = 0
silver_count = 0
gold_count = 0

for index, row in df.iterrows():
    
    athlete = row['Athlete']
    year = row['Year']
    event = row['Event']
    medal = row['Medal']

    if athlete == prev:
        continue

    else:
        if medal == "Bronze": bronze_count += 1
        elif medal == "Silver": silver_count += 1
        elif medal == "Gold": gold_count += 1

prob_b = bronze_count/rows
prob_s = silver_count/rows
prob_g = gold_count/rows 

