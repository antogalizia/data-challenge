from fastapi import APIRouter, HTTPException, status
from app.services import extract_data, processed_data, clean_data

router = APIRouter()

#@router.get("/extraction", status_code=status.HTTP_200_OK)
#def extract():
#    data = extract_data()
#    return {"data": data}


@router.get("/processed", status_code=status.HTTP_200_OK)
def get_processed():
    try:
        data = processed_data()
        return {"data": data}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay datos extraídos en data/raw")


@router.get("/processed/products", status_code=status.HTTP_200_OK)
def get_processed_products():
    try:
        data = processed_data()
        return {"data": data["products"]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay datos extraídos en data/raw")


@router.get("/processed/sellers", status_code=status.HTTP_200_OK)
def get_processed_sellers():
    try:
        data = processed_data()
        return {"data": data["sellers"]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay datos extraídos en data/raw")


@router.get("/processed/shipments", status_code=status.HTTP_200_OK)
def get_processed_shipments():
    try:
        data = processed_data()
        return {"data": data["shipments"]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay datos extraídos en data/raw")
    

@router.get("/cleaned/products", status_code=status.HTTP_200_OK)
def get_cleaned_products():
    try:
        data = clean_data()
        return {"data": data["products"]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay datos extraídos en data/processed")


@router.get("/cleaned/sellers", status_code=status.HTTP_200_OK)
def get_cleaned_sellers():
    try:
        data = clean_data()
        return {"data": data["sellers"]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay datos extraídos en data/processed")


@router.get("/cleaned/shipments", status_code=status.HTTP_200_OK)
def get_cleaned_shipments():
    try:
        data = clean_data()
        return {"data": data["shipments"]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No hay datos extraídos en data/processed")
