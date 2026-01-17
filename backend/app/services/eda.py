import pandas as pd
import os

PROCESSED_DIR = "data/processed"

def load_cleaned_data():
    path = os.path.join(PROCESSED_DIR, "cleaned_data.csv")
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)

def dataset_summary():
    df = load_cleaned_data()
    if df is None:
        return {"error": "No cleaned dataset found"}

    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_total": int(df.isnull().sum().sum()),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    return summary

def correlation_matrix():
    df = load_cleaned_data()
    if df is None:
        return {"error": "No cleaned dataset found"}

    num_df = df.select_dtypes(include="number")
    corr = num_df.corr().fillna(0)
    return corr.to_dict()
