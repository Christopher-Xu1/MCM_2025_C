import pandas as pd
from pathlib import Path

folder_path = Path('../Data/processed_olympics_data/')

output_file = 'new_athlete_probabilities.csv'
output_df = pd.DataFrame(columns=['Country', 'Gender', 'Event', 'prob_bronze', 'prob_silver', 'prob_gold'])
data_list = []


for file in folder_path.iterdir():
    print(file)
    df = pd.read_csv(file)
    rows = df.shape[0]

    # df['First event'] = 'default_value'  # Set a default value for all rows

    for index, row in df.iterrows():
        
        athlete = row['Athlete']
        year = row['Year']
        event = row['Event']
        medal = row['Medal']
        

        is_first_event = True
        for i, r in df.iterrows():
            if athlete == r['Athlete'] and r['Year'] < year:
                # df['First Event'] = "True"
                is_first_event = False
                break
                
    
        df.loc[index, 'First Event'] = "True"  if is_first_event else "False"

    df.to_csv(file, index = False)

    # if file.is_file():
    #     print(f"Processing file: {file}")

# output_df = pd.DataFrame(data_list)
# output_df.to_csv(output_file, index=False)

