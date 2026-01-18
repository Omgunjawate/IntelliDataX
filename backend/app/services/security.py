import pandas as pd
import re

def mask_pii(df: pd.DataFrame) -> pd.DataFrame:
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern = r"\b\d{10}\b"

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str)

            df[col] = df[col].apply(
                lambda x: re.sub(email_pattern, "[EMAIL_MASKED]", x)
            )
            df[col] = df[col].apply(
                lambda x: re.sub(phone_pattern, "[PHONE_MASKED]", x)
            )

    return df
