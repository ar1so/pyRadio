from database import load_database
from file_processor import select_or_create_csv, process_file

def main():
    database = load_database()
    output_csv = select_or_create_csv(database)
    
    while True:
        print("\n--- New File Processing ---")
        if not process_file(output_csv, database):
            break
    
    print("Program finished. Thank you for using the radiomics feature extractor.")

if __name__ == "__main__":
    main()