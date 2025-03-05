from extraction.extract import get_data
from transformation.transform import cleaning, create_tables

API_URL = "https://api.mercadolibre.com/sites/MLA/search"
params = {"q": "chromecast", "limit": 50}

def main():
    try:
        get_data(API_URL, num_requests=10, params=params, save_to="raw")
        create_tables('data/raw/data.json')
        cleaning()
        
    except Exception as e:
        print(f"Error en el pipeline: {e}")

if __name__ == "__main__":
    main()