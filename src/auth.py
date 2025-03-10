import os
import requests
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


def get_token(code):
    url = 'https://api.mercadolibre.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data.get('access_token')
    else:
        print(f'Error al obtener el token: {response.status_code}, {response.text}')
        return None
