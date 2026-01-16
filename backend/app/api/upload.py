from fastapi import APIRouter, UploadFile, File
import pandas as pd
import os

router = APIRouter()

UPLOAD_DIR = "data/raw"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns)
    }
