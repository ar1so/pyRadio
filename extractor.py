import os
import pandas as pd
from datetime import datetime
from database import add_patient_info, add_csv_file
from radiomics_extractor import extract_radiomics_features

def process_file(output_csv, database):
    image_path = input("Please drag and drop the image file here and press Enter (or type 'quit' to exit): ").strip()
    if image_path.lower() == 'quit':
        return False

    mask_path = input("Please drag and drop the mask file here and press Enter: ").strip()
    label = int(input("Please enter the label (integer): "))
    sequence_name = input("Please enter the sequence name: ")
    patient_name = input("Please enter the patient's name: ")

    add_patient_info(database, patient_name, image_path, mask_path, label, sequence_name)

    features = extract_radiomics_features(image_path, mask_path, label, sequence_name, patient_name)

    if features is not None:
        if os.path.exists(output_csv):
            existing_data = pd.read_csv(output_csv)
            updated_data = pd.concat([existing_data, features], ignore_index=True)
        else:
            updated_data = features

        updated_data.to_csv(output_csv, index=False)
        print(f"Features saved to {output_csv}")
    else:
        print("Failed to extract features. Moving to next file.")

    return True

def select_or_create_csv(database):
    if not database['csv_files']:
        print("No existing CSV files found.")
    else:
        print("\nExisting CSV files:")
        for i, (name, path) in enumerate(database['csv_files'].items(), 1):
            print(f"{i}. {name} ({path})")
    
    choice = input("\nEnter the number of an existing CSV file or press Enter to create a new one: ")
    
    if choice.isdigit() and 1 <= int(choice) <= len(database['csv_files']):
        return list(database['csv_files'].values())[int(choice) - 1]
    else:
        new_csv = input("Enter the path for the new CSV file: ")
        add_csv_file(database, new_csv)
        return new_csv