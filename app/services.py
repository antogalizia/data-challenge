from src.etl import Extract, Transform
import os

API_URL = "https://api.mercadolibre.com/sites/MLA/search"
params = {"q": "chromecast", "limit": 50}

def extract_data(access_token):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")

    extract = Extract(client_id, client_secret, redirect_uri)
    extract.access_token = access_token  # Asignamos el token de acceso
    return extract.get_data(API_URL, num_requests=10, params=params, save_to="raw")


"""
def extract_data():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")

    extract = Extract(client_id, client_secret, redirect_uri)
    #extract.set_code(code)  # Paso el código de autorización a la clase Extract
    return extract.get_data(API_URL, num_requests=10, params=params, save_to="raw")
"""
def processed_data():
    transform = Transform()
    return transform.parsed_data()

def clean_data():
    transform = Transform()
    return transform.cleaning()