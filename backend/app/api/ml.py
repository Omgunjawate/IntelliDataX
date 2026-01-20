from fastapi import APIRouter
import pandas as pd
import os

from backend.app.services.ml_engine import detect_target_column, decide_problem_type

router = APIRouter(prefix="/ml", tags=["ML"])

DATA_PATH = "data/processed/cleaned_data.csv"


@router.get("/analyze")
def analyze_dataset_for_ml():
    if not os.path.exists(DATA_PATH):
        return {"error": "Cleaned dataset not found."}

    df = pd.read_csv(DATA_PATH)

    target = detect_target_column(df)
    if target is None:
        return {"message": "No suitable target column detected for ML."}

    problem_type = decide_problem_type(df, target)

    return {
        "suggested_target": target,
        "problem_type": problem_type,
        "message": f"A {problem_type} problem can be formulated using '{target}' as the target variable."
    }
