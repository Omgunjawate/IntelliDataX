from fastapi import FastAPI


from backend.app.api import upload, preprocess, eda



app = FastAPI(title="IntelliDataX API")

app.include_router(upload.router)
app.include_router(preprocess.router)

app.include_router(eda.router)

@app.get("/")
def root():
    return {"status": "IntelliDataX backend running"}
