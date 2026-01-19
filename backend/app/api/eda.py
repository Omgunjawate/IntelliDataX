from fastapi import APIRouter
import pandas as pd
import os

from backend.app.services.insight_engine import generate_insights

router = APIRouter(prefix="/eda", tags=["EDA"])

DATA_PATH = "data/processed/cleaned_data.csv"


@router.get("/summary")
def summary():
    df = pd.read_csv(DATA_PATH)
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_total": int(df.isnull().sum().sum()),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }


@router.get("/correlation")
def correlation():
    df = pd.read_csv(DATA_PATH)
    corr = df.select_dtypes(include="number").corr()
    return corr.fillna(0).to_dict()


@router.get("/missing")
def missing_values():
    df = pd.read_csv(DATA_PATH)
    return df.isnull().sum().to_dict()


from backend.app.services.insight_engine import generate_insights
import os
import pandas as pd

@router.get("/insights")
def insights():
    if not os.path.exists(DATA_PATH):
        return {"error": "Cleaned dataset not found. Please preprocess data first."}

    df = pd.read_csv(DATA_PATH)
    insights = generate_insights(df)

    return {
        "count": len(insights),
        "insights": insights
    }

