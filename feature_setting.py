import pandas as pd
from radiomics import featureextractor
import traceback
import os

def extract_radiomics_features(image_path, mask_path, label, sequence_name, patient_name):
    try:
        extractor = featureextractor.RadiomicsFeatureExtractor()
        result = extractor.execute(image_path, mask_path, label=label)
        df = pd.DataFrame([result])
        df['SequenceName'] = sequence_name
        df['ImagePath'] = image_path
        df['MaskPath'] = mask_path
        df['FileName'] = os.path.basename(image_path)
        df['Label'] = label
        df['PatientName'] = patient_name
        return df
    except Exception as e:
        print(f"Error processing file {image_path}:")
        print(str(e))
        print(traceback.format_exc())
        return None