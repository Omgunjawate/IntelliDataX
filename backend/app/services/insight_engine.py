import pandas as pd

def generate_insights(df: pd.DataFrame):
    insights = []

    IGNORED_PATTERNS = ["zero", "dummy", "onehot", "encoded"]

    # ---------- Dataset size ----------
    rows, cols = df.shape
    if rows < 100:
        insights.append({
            "severity": "info",
            "message": "This is a small dataset. Insights may be limited but easy to explore."
        })
    elif rows > 100_000:
        insights.append({
            "severity": "info",
            "message": "This is a large dataset. Consider filtering or sampling for faster analysis."
        })

    # ---------- Missing values ----------
    missing_ratio = df.isnull().mean()
    for col, ratio in missing_ratio.items():
        if ratio > 0.5:
            insights.append({
                "severity": "critical",
                "message": f"Column '{col}' has more than 50% missing values."
            })
        elif ratio > 0.2:
            insights.append({
                "severity": "warning",
                "message": f"Column '{col}' has significant missing values ({int(ratio*100)}%)."
            })

    # ---------- Low variance (filtered) ----------
    for col in df.select_dtypes(include="number").columns:
        if any(p in col.lower() for p in IGNORED_PATTERNS):
            continue
        if df[col].nunique() <= 1:
            insights.append({
                "severity": "info",
                "message": f"Column '{col}' has almost no variation and may not be useful."
            })

    # ---------- Correlation ----------
    corr = df.select_dtypes(include="number").corr()
    for i in corr.columns:
        for j in corr.columns:
            if i != j and abs(corr.loc[i, j]) > 0.85:
                insights.append({
                    "severity": "info",
                    "message": f"Strong relationship detected between '{i}' and '{j}'."
                })

    # ---------- Categorical dominance ----------
    cat_cols = df.select_dtypes(include="object").columns
    if len(cat_cols) > len(df.columns) * 0.6:
        insights.append({
            "severity": "info",
            "message": "Most columns are categorical. Count-based charts will be more meaningful than correlations."
        })

    # ---------- Date-like columns ----------
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            insights.append({
                "severity": "info",
                "message": f"Column '{col}' appears to represent time. Trend analysis may reveal patterns."
            })

    if not insights:
        insights.append({
            "severity": "info",
            "message": "This dataset appears clean and well-structured with no major issues."
        })

    return insights
