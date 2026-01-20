import pandas as pd

def detect_target_column(df: pd.DataFrame):
    """
    Heuristically detect a possible target column.
    Preference order:
    1. Columns with names like target, label, price, sales, rating
    2. Numeric columns with reasonable variance
    """

    candidate_keywords = ["target", "label", "price", "sales", "rating", "score"]

    for col in df.columns:
        if any(k in col.lower() for k in candidate_keywords):
            return col

    numeric_cols = df.select_dtypes(include="number")
    if not numeric_cols.empty:
        return numeric_cols.columns[-1]

    return None


def decide_problem_type(df: pd.DataFrame, target_col: str):
    """
    Decide regression or classification based on target column.
    """
    if df[target_col].dtype == "object":
        return "classification"

    unique_vals = df[target_col].nunique()
    if unique_vals <= 10:
        return "classification"

    return "regression"
