from fastapi import FastAPI
from backend.app.api import upload, preprocess

app = FastAPI(title="IntelliDataX API")

app.include_router(upload.router)
app.include_router(preprocess.router)

@app.get("/")
def root():
    return {"status": "IntelliDataX backend running"}
