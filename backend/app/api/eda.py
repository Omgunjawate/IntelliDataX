from fastapi import APIRouter
from backend.app.services.eda import dataset_summary, correlation_matrix

router = APIRouter()

@router.get("/eda/summary")
def get_summary():
    return dataset_summary()

@router.get("/eda/correlation")
def get_correlation():
    return correlation_matrix()
