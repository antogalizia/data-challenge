from src.etl import Extract, Transform

API_URL = "https://api.mercadolibre.com/sites/MLA/search"
params = {"q": "chromecast", "limit": 50}

def extract_data():
    extract = Extract()
    return extract.get_data(API_URL, num_requests=10, params=params, save_to="raw")

def processed_data():
    transform = Transform()
    return transform.parsed_data()

def clean_data():
    transform = Transform()
    return transform.cleaning()