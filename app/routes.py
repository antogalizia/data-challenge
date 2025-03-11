from fastapi import APIRouter, HTTPException, status, Request, Header
from fastapi.responses import RedirectResponse
from app.services import extract_data, processed_data, clean_data
from src.auth import get_token
import os

router = APIRouter()
CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")


@router.get("/")
async def authorize():
    """
    Redirige al usuario a la URL de autorización de Mercado Libre.
    """
    auth_url = f"https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return RedirectResponse(auth_url)


@router.get("/callback")
async def callback(request: Request):
    """
    Captura el código de autorización desde la URL y obtiene el token de acceso.
    """
    code = request.query_params.get("code")  # Captura el código de autorización

    if not code:
        raise HTTPException(status_code=400, detail="No se recibió código de autorización")

    access_token = get_token(code)  # Obtiene el token de Mercado Libre

    if access_token:
        return {"message": "Token obtenido", "access_token": access_token}
    else:
        raise HTTPException(status_code=500, detail="Error al obtener el token")


@router.get("/extraction", status_code=status.HTTP_200_OK)
def extract(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Token de autorización no proporcionado correctamente.")

    access_token = authorization.split("Bearer ")[1]  # Extrae el token del header

    data = extract_data(access_token)
    return {"data": data}


"""
@router.get("/extraction", status_code=status.HTTP_200_OK)
def extract(access_token: str):
    
    Extrae los datos usando el access_token obtenido en /callback.
    
    if not access_token:
        raise HTTPException(status_code=400, detail="No se proporcionó un token de acceso.")

    data = extract_data(access_token)
    return {"data": data}
"""


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
