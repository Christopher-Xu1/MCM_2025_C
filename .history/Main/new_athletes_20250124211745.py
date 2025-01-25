# scripts/data_processing.py

import pandas as pd
import os
import re

# Function to sanitize filenames by replacing invalid characters with underscores
def sanitize_filename(name):
    """
    Replace any character that is not a word character, hyphen, or underscore with an underscore.

    Parameters:
        name (str): The original filename string.

    Returns:
        str: The sanitized filename string.
    """
    return re.sub(r'[^\w\-]', '_', name)

# Function to load sports mapping
def load_sports_mapping(mapping_file_path):
    """
    Load the sports mapping from a CSV file.

    Parameters:
        mapping_file_path (str): Path to the sports mapping CSV file.

    Returns:
        pd.DataFrame: DataFrame containing sports mapping.
    """
    try:
        sports_mapping = pd.read_csv(mapping_file_path)
        print(f"Loaded sports mapping from {mapping_file_path}")
        return sports_mapping
    except FileNotFoundError:
        print(f"Error: The mapping file '{mapping_file_path}' does not exist.")
        exit(1)

def main():
    # Define paths
    raw_data_path = os.path.join('data', 'raw', 'summerOly_athletes.csv')  # Path to the main data file
    mapping_file_path = os.path.join('data', 'raw', 'sports_codes.csv')  # Path to the sports mapping file
    processed_dir = os.path.join('data', 'processed')  # Directory to save processed files
    os.makedirs(processed_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Define a mapping for country name standardization
    country_mapping = {
        "USA": "United States",
        "U.S.A.": "United States",
        "Great Britain": "United Kingdom",
        "Soviet Union": "Russia",
        "Ain": "Russia"  # Added as per your mapping
        # Add more mappings if necessary
    }

    # Load the main data
    try:
        data = pd.read_csv(raw_data_path, header=None, names=[
            "Athlete", "Gender", "Country", "Country Code", "Year", "City", 
            "Sport", "Event", "Medal"
        ])
        print(f"Loaded data from {raw_data_path}")
    except FileNotFoundError:
        print(f"Error: The file '{raw_data_path}' does not exist.")
        exit(1)

    # Normalize and map country names to ensure consistency
    data["Country"] = data["Country"].str.strip().str.title()
    data["Country"] = data["Country"].replace(country_mapping)
    print("Standardized country names.")

    # Load sports mapping
    sports_mapping = load_sports_mapping(mapping_file_path)

    # Check if 'Sport' and 'Code' columns exist in sports_mapping
    if 'Sport' not in sports_mapping.columns or 'Code' not in sports_mapping.columns:
        print("Error: 'Sport' and/or 'Code' columns are missing in sports_codes.csv.")
        exit(1)

    # Create a dictionary for sport renaming (Sport to Code)
    sport_to_code = pd.Series(sports_mapping.Code.values, index=sports_mapping.Sport).to_dict()

    # Apply the sport code mapping
    data['Sport_Code'] = data['Sport'].map(sport_to_code)

    # For sports not found in the mapping, retain the original 'Sport' name
    data['Sport_Code'] = data['Sport_Code'].fillna(data['Sport'])
    print("Applied sports code mapping.")

    # Identify sports that were not mapped (i.e., retained original names)
    mapped_codes = set(sports_mapping.Code)
    data_codes_unique = set(data['Sport_Code'].unique())
    # Exclude original sport names that were retained due to missing mapping
    # This assumes that 'Code' is unique and different from any 'Sport' name
    unmapped_codes = data_codes_unique - mapped_codes
    if len(unmapped_codes) > 0:
        print(f"Warning: The following sports were not mapped and retained their original names: {unmapped_codes}")

    # Process data by grouping
    for (country, sport_code, gender), group in data.groupby(["Country", "Sport_Code", "Gender"]):
        # Sanitize country and sport code names to avoid invalid characters
        country_sanitized = sanitize_filename(country)
        sport_code_sanitized = sanitize_filename(str(sport_code))
        gender_label = "mens" if gender == "M" else "womens"

        # Construct the filename using the Sport Code
        filename = f"{country_sanitized}_{sport_code_sanitized}_{gender_label}.csv"
        filepath = os.path.join(processed_dir, filename)

        # Add meta-label for athletes competing multiple times
        group["Multiple Events"] = group["Athlete"].duplicated(keep=False)

        try:
            # Save the group to its CSV file
            group.to_csv(filepath, index=False)
            print(f"Saved processed data to {filepath}")
        except OSError as e:
            print(f"Error saving file '{filepath}': {e}")

    print(f"All processed data has been saved to the '{processed_dir}' directory.")

if __name__ == "__main__":
    main()
