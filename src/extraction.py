import requests
import json

def get_data(url, num_requests, params=None, output_file="data.json"):
    """
    Función de extracción que realiza múltiples solicitudes GET a una API y guarda los datos en un JSON.

    Parámetros:
    url(str): url de la API que en este caso incluye los parámetros de ruta
    num_requests(int): cantidad de peticiones 
    output_file(str): 

    Retorna:
    output_file(str): JSON de respuesta
    """

    data = []  
    try:
        for i in range(num_requests):
            # Corrección de paginación en cada iteración
            params.update({"offset": i * 50})  
            # Solicitud GET para la obtención de datos
            response = requests.get(url, params=params)
            response.raise_for_status()

            try:
                # Codificación a JSON y extracción de key de resultados
                json_response = response.json()
                results = json_response.get("results", []) 

                if isinstance(results, list):
                    data.extend(results)  
                else:
                    print(f"Error: 'results' no es una lista en la página {i}")

            except requests.exceptions.JSONDecodeError:
                print(f"Error al decodificar JSON en la página {i}")

    except requests.exceptions.RequestException as err:
        print(f"La petición ha fallado. Código de error: {err}")
        return None


    if data:
        # Se guarda el contenido de data en el JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return output_file 
    else:
        return None 



