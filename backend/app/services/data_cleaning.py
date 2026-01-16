import pandas as pd
import os

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def get_latest_csv(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    return os.path.join(directory, files[0])

def clean_data(remove_duplicates=True, fill_missing=True):
    raw_file = get_latest_csv(RAW_DIR)
    if raw_file is None:
        return {"error": "No dataset found"}

    df = pd.read_csv(raw_file)
    original_rows = len(df)
    original_missing = df.isnull().sum().sum()

    if remove_duplicates:
        df = df.drop_duplicates()

    if fill_missing:
        for col in df.select_dtypes(include=["number"]).columns:
            df[col].fillna(df[col].mean(), inplace=True)

    cleaned_rows = len(df)
    cleaned_missing = df.isnull().sum().sum()

    output_path = os.path.join(PROCESSED_DIR, "cleaned_data.csv")
    df.to_csv(output_path, index=False)

    return {
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "original_missing": int(original_missing),
        "cleaned_missing": int(cleaned_missing),
        "output_file": output_path
    }
