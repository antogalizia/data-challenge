# auth.py
import requests

def obtener_token(client_id, client_secret, code, redirect_uri):
    url = 'https://api.mercadolibre.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data.get('access_token')
    else:
        print(f'Error al obtener el token: {response.status_code}, {response.text}')
        return None
