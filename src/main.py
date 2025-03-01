from extraction.extract import get_data

API_URL = "https://api.mercadolibre.com/sites/MLA/search"
params = {"q": "chromecast", "limit": 50}

def main():
    get_data(API_URL, num_requests=10, params=params, save_to="raw")
    

if __name__ == "__main__":
    main()