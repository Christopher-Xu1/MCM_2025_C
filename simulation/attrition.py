import pandas as pd
from pathlib import Path

folder_path = Path('../Data/processed_olympics_data/')


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
    