import pandas as pd
from pathlib import Path

folder_path = Path('../Data/processed_olympics_data/')

output_file = 'new_athlete_probabilities.csv'
output_df = pd.DataFrame(columns=['Country', 'Gender', 'Event', 'prob_bronze', 'prob_silver', 'prob_gold'])
data_list = []


codes = ["SWA",
"DIV",
"OWS",
"SWM",
"WPO",
"ARC",
"ATH",
"BDM",
"BSB",
"SBL",
"BK3",
"BKB",
"PEL",
"BOX",
"BKG",
"CSP",
"CSL",
"CKT",
"CQT",
"BMF",
"BMX",
"MTB",
"CRD",
"CTR",
"EDR",
"EVE",
"EJP",
"EVL",
"EDV",
"FEN",
"HOC",
"AFB",
"FBL",
"GLF",
"GAR",
"GRY",
"GTR",
"HBL",
"HBL",
"JUD",
"KTE",
"LAX",
"LAX",
"MPN",
"POL",
"RQT",
"ROQ",
"ROC",
"ROW",
"RU7",
"RUG",
"SAL",
"SHO",
"SKB",
"CLB",
"SQU",
"SRF",
"SWA",
"TTE",
"TKW",
"TEN",
"TRI",
"TOW",
"VBV",
"VVO",
"PBT",
"PBT",
"WLF",
"WRF",
"WRG",
"FSK",
"FSK",
"IHO",
"JDP",
"ART",
"ALP",
"AER",
]

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
        
        if row['Year'] == 2024:
            rows -= 1
            continue

        if row['First Event'] == True:
            if medal == "Bronze": bronze_count += 1
            elif medal == "Silver": silver_count += 1
            elif medal == "Gold": gold_count += 1

    if rows == 0:
        prob_b = "undef"
        prob_s = "undef"
        prob_g = "undef"
        continue
    prob_b = bronze_count/rows
    prob_s = silver_count/rows
    prob_g = gold_count/rows 

    df = df.reset_index(drop=True)
    # event_r = df['Event'].iloc[0]
    # if event_r == "Men":
    #     print(file)

    headers = str(file).split("/")[-1]
    parts = headers.split("_")
    for i in parts:
        if i in codes: 
            event_t = i
            break
    # event_t = ' '.join(parts[1:-1])

    country = df['Country Code'].iloc[0]
    gender = df['Gender'].iloc[0]

    data_list.append({
            'Country Code': country,
            'Gender': gender,
            'Event': event_t,
            'bronze' : bronze_count,
            'silver' : silver_count,
            'gold' : gold_count,
            'total athletes' : rows,
            'prob_bronze': prob_b,
            'prob_silver': prob_s,
            'prob_gold': prob_g,
            'raw medals': bronze_count + silver_count + gold_count
        })

    # if file.is_file():
    #     print(f"Processing file: {file}")

output_df = pd.DataFrame(data_list)
output_df.to_csv(output_file, index=False)