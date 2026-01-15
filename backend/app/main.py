from fastapi import FastAPI

app = FastAPI(title="IntelliDataX API")

@app.get("/")
def root():
    return {"status": "IntelliDataX backend running"}
