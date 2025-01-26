import pandas as pd
from pathlib import Path

folder_path = Path('../Data/processed_olympics_data/')

output_file = '2024_athletes.csv'
output_df = pd.DataFrame(columns=['Country', 'Gender', 'Event', 'prob_bronze', 'prob_silver', 'prob_gold'])
data_list = []


for file in folder_path.iterdir():

    df = pd.read_csv(file)


    for index, row in df.iterrows():

        if row['Year'] == 2024:
            data_list.append({
                'Athlete' : row['Athlete'],
                'Country' : row['Country Code'],
                'Event' : row['Event Code'],
                'First event' : row['First Event'],
                'Gender' : row['Gender']
            })
    

output_df = pd.DataFrame(data_list)
output_df.to_csv(output_file, index=False)