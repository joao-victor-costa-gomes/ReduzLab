import os
import pandas as pd
from flask import current_app

def extract_sample(dataset_path, sample_rate=1.0):
    
    print(f"📂 Reading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path, delimiter=",")
    print(f"✅ Dataset loaded with {len(df)} rows")

    sample_size = int(len(df) * sample_rate)
    print(f"🎯 Sampling {sample_size} rows ({sample_rate * 100:.0f}%)")

    sample = df.sample(n=sample_size, random_state=42)

    # Prepare the output filename
    original_filename = os.path.basename(dataset_path)
    name_without_ext = os.path.splitext(original_filename)[0]
    output_filename = f"{name_without_ext}_sample.csv"

    # Ensure the samples folder exists
    samples_folder = current_app.config['SAMPLES_FOLDER']
    if not os.path.exists(samples_folder):
        os.makedirs(samples_folder)

    output_path = os.path.join(samples_folder, output_filename)
    sample.to_csv(output_path, index=False)

    return output_path
