from fastapi import APIRouter
from app.services import extract_data

router = APIRouter()

@router.get("/extraction")
def extract():
    data = extract_data()
    return {"status": "success", "data": data}



