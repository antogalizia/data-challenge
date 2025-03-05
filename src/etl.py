import requests

class Extract:
    def get_data(self, url, num_requests, params=None, save_to="raw"):
        """
        Función de extracción que realiza múltiples solicitudes GET a una API y guarda los datos en un JSON.

        Parámetros:
        url(str): url de la API que en este caso incluye los parámetros de ruta
        num_requests(int): cantidad de peticiones 
        params(dict): parámetros de consulta
        save_to (str): subdirectorio dentro de "data/" donde se guardarán los datos

        Retorna:
        output_file(str): JSON de respuesta
        """

        data = []  

        for i in range(num_requests):
            try:
                # Corrección de paginación en cada iteración
                params.update({"offset": i * 50})  
                
                # Solicitud GET para la obtención de datos
                response = requests.get(url, params=params)
                response.raise_for_status()

                try:
                    # Codificación a JSON y extracción de key de resultados
                    json_response = response.json()
                    results = json_response.get("results", []) 
                    
                    # Se agregan los datos a la lista 
                    if isinstance(results, list):
                        data.extend(results)  
                    else:
                        print(f"Error: 'results' no es una lista en la página {i}")

                except requests.exceptions.JSONDecodeError:
                    print(f"Error al decodificar JSON en la página {i}")

            except requests.exceptions.RequestException as e:
                print(f"Falló en la solicitud GET en la página {i}: {e}")
                continue 

        
            #file_name = "data.json"  
            #saved_path = load_data(data, file_name, save_to)
        if data:
            return data
        else:
            return None 
        

