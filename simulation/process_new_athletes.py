import pandas as pd
from pathlib import Path

folder_path = Path('../Data/processed_olympics_data/')

output_file = 'new_athlete_probabilities.csv'
output_df = pd.DataFrame(columns=['Country', 'Gender', 'Event', 'prob_bronze', 'prob_silver', 'prob_gold'])
data_list = []


for file in folder_path.iterdir():

    df = pd.read_csv(file)
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

    df = df.reset_index(drop=True)
    event_r = df['Event'].iloc[0]
    if event_r == "Men":
        print(file)

    country = df['Country'].iloc[0]
    gender = df['Gender'].iloc[0]

    data_list.append({
            'Country': country,
            'Gender': gender,
            'Event': event_r,
            'prob_bronze': prob_b,
            'prob_silver': prob_s,
            'prob_gold': prob_g
        })

    # if file.is_file():
    #     print(f"Processing file: {file}")

output_df = pd.DataFrame(data_list)
output_df.to_csv(output_file, index=False)