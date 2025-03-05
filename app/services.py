from src.etl import Extract

API_URL = "https://api.mercadolibre.com/sites/MLA/search"
params = {"q": "chromecast", "limit": 50}

def extract_data():
    extractor = Extract()
    return extractor.get_data(API_URL, num_requests=10, params=params, save_to="raw")

