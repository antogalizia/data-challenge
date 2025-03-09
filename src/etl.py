from pathlib import Path
from fastapi import HTTPException
import json
import uuid
import pandas as pd
import requests
import os 


class Extract:

    def get_data(self, url, num_requests, params=None, save_to="raw"):
        """
        Función de extracción que realiza múltiples solicitudes GET a una API y guarda los datos en data/raw.

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
                if params is None:
                    params = {}

                # Corrección de paginación en cada iteración
                params.update({"offset": i * 50})  
                
                # Solicitud GET para la obtención de datos
                response = requests.get(url, params=params)

                if response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Recurso no encontrado")
                
                response.raise_for_status()

                # Codificación a JSON y extracción de key de resultados
                json_response = response.json()
                results = json_response.get("results", []) 

                if not isinstance(results, list):
                    raise ValueError(f"'results' no es una lista en la página {i}")
                    
                data.extend(results)  
                    
            except requests.exceptions.RequestException as e:
                print(f"Error en solicitud GET en la página {i}: {e}")
                raise  
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error en la estructura de datos en la página {i}: {e}")
                raise

        # Instancio la clase Load para guardar los datos
        loader = Load()
        file_name = "data.json"  
        loader.load_data(data, file_name, save_to)
        return data
        
class Transform:

    def get_attribute_value(self, attributes, key):
        """
        Función auxiliar para obtener el valor de un atributo específico.
        """
        for attr in attributes:
            if attr.get("id") == key:
                return attr.get("value_name", None)
        return None

    def parsed_data(self):
        """
        Función que realiza el parseo de los datos al modelo relacional.
        """

        data_raw_path = "data/raw/data.json"
        products, sellers, shipments = [], [], []

        # Leer los datos desde el archivo JSON en data/raw
        try:
            with open(data_raw_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo {data_raw_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error en la estructura del archivo JSON {data_raw_path}: {e}")

        for elem in data:
            attributes = elem.get("attributes", [])

            products.append({
                "product_id": elem["id"],
                "seller_id": elem["seller"]["id"],
                "title": elem["title"],
                "price": elem["price"],
                "available_quantity": elem["available_quantity"],
                "condition": elem["condition"],
                "brand": self.get_attribute_value(attributes, "BRAND"),
                "model": self.get_attribute_value(attributes, "MODEL")
            })

            sellers.append({
                "seller_id": elem["seller"]["id"],
                "name": elem["seller"]["nickname"],
                "state": elem["address"]["state_name"],
                "city": elem["address"]["city_name"]
            })

            shipments.append({
                "shipping_id": str(uuid.uuid4()),
                "product_id": elem["id"],
                "store_pick_up": elem["shipping"]["store_pick_up"],
                "free_shipping": elem["shipping"]["free_shipping"],
                "logistic_type": elem["shipping"]["logistic_type"]
            })

        tables = {"products": products, "sellers": sellers, "shipments": shipments}
    
        # Instancio la clase Load para guardar los datos
        loader = Load()
        for name, data in tables.items():
            loader.load_data(data, f"{name}.json", "processed")
        
        return tables
    
    def cleaning(self):
        input_dir = Path("data/processed") 
        output_dir = "clean"
        cleaned_data = {}

        # Reglas de limpieza según archivo
        CLEANING_RULES = {
            "products": {"id_column": "product_id", "required_columns": ["product_id", "seller_id", "title"]},
            "shipments": {"id_column": "shipping_id", "required_columns": ["shipping_id", "product_id"]},
            "sellers": {"id_column": "seller_id", "required_columns": ["seller_id", "name"]}
        }
        
        # Itero sobre cada archivo en processed/
        for file_path in input_dir.glob("*.json"):  
            # Nombre sin extensión
            file_name = file_path.stem  

            # Verifico si hay reglas definidas para este archivo
            if file_name not in CLEANING_RULES:
                continue
            
            # Obtengo las reglas específicas del archivo actual
            rules = CLEANING_RULES[file_name]  

            try:
                # Cargo el JSON a un dataframe
                df = pd.read_json(file_path, orient="records")

                # Limpieza dinámica según las reglas
                df.dropna(subset=rules["required_columns"], inplace=True)
                df.drop_duplicates(subset=[rules["id_column"]], keep="first", inplace=True)         
                
                # Convierto el dataframe a lista de diccionarios
                json_data = df.to_dict(orient="records")

                # Almacenamiento
                loader = Load()
                loader.load_data(json_data, f"{file_name}.json", output_dir)

                # Agrego los datos limpios al diccionario de retorno
                cleaned_data[file_name] = json_data

            except json.JSONDecodeError as e:
                raise ValueError(f"Error en {file_name}.json: formato JSON inválido - {e}")
            except Exception as e:
                print(f"Error inesperado en {file_name}.json: {e}")

        return cleaned_data

class Load:

    def load_data(self, json_data: dict, file_name: str, relative_path: str):
        """
        Guarda un JSON en el directorio 'data/' dentro del proyecto.

        Parámetros:
        json_data(dict): el contenido que se va a almacenar
        file_name(str): nombre del archivo con extensión .json
        relative_path(str): ruta relativa al destino final del archivo

        Retorna:
        Ruta completa donde se guardó el archivo
        """

        # Ruta completa del destino de los datos
        directory = Path("data") / relative_path

        # Creación del directorio
        directory.mkdir(parents=True, exist_ok=True)

        # Ruta completa del JSON
        file_path = directory / file_name

        try:
            # Escritura del archivo
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

        except (OSError, json.JSONDecodeError) as e:
            raise OSError(f"Error al guardar el archivo JSON: {e}")
              
    def load_ndjson(json_data: dict, file_name: str, relative_path: str):

        # Ruta completa del destino de los datos
        directory = Path("data") / relative_path

        # Creación del directorio
        directory.mkdir(parents=True, exist_ok=True)

        # Ruta completa del JSON
        file_path = directory / file_name

        try:
            with file_path.open("w", encoding="utf-8") as f:
                for obj in json_data:
                    # Escribo cada objeto en una nueva línea
                    f.write(json.dumps(obj) + "\n")  

        except (OSError, json.JSONDecodeError) as e:
            raise OSError(f"Error al guardar el archivo JSON: {e}")
              