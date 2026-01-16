from fastapi import APIRouter
from backend.app.services.data_cleaning import clean_data

router = APIRouter()

@router.post("/clean")
def run_cleaning(remove_duplicates: bool = True, fill_missing: bool = True):
    result = clean_data(remove_duplicates, fill_missing)
    return result
