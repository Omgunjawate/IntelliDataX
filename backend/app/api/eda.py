from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/eda", tags=["EDA"])

DATA_PATH = "data/processed/cleaned_data.csv"


@router.get("/summary")
def summary():
    try:
        df = pd.read_csv(DATA_PATH)

        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_total": int(df.isnull().sum().sum()),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }

    except Exception as e:
        return {"error": str(e)}


@router.get("/correlation")
def correlation():
    try:
        df = pd.read_csv(DATA_PATH)
        corr = df.select_dtypes(include="number").corr()
        return corr.fillna(0).to_dict()
    except Exception as e:
        return {"error": str(e)}


@router.get("/missing")
def missing_values():
    try:
        df = pd.read_csv(DATA_PATH)
        missing = df.isnull().sum()
        return missing.to_dict()
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/insights")
def insights():
    try:
        df = pd.read_csv(DATA_PATH)
        insights = []

        # Missing values insight
        missing = df.isnull().mean()
        for col, ratio in missing.items():
            if ratio > 0.3:
                insights.append(f"Column '{col}' has more than 30% missing values.")

        # Correlation insight
        corr = df.select_dtypes(include="number").corr()
        for col in corr.columns:
            for idx in corr.index:
                if col != idx and abs(corr.loc[idx, col]) > 0.8:
                    insights.append(
                        f"Strong correlation detected between '{col}' and '{idx}'."
                    )

        return {"insights": list(set(insights))}

    except Exception as e:
        return {"error": str(e)}

