from load.load import load_ndjson, load_data
from pathlib import Path
import json
import uuid
import pandas as pd


def cleaning():
    input_dir = Path("data/processed") 
    output_dir = "clean"

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

            # Almacenamiento
            json_data = df.to_dict(orient="records")
            load_ndjson(json_data, f"{file_name}.json", output_dir)

        except json.JSONDecodeError as e:
            print(f"Error en {file_name}.json: formato JSON inválido - {e}")
        except Exception as e:
            print(f"Error inesperado en {file_name}.json: {e}")



# Función auxiliar para obtener el valor de un atributo específico
def get_attribute_value(attributes, key):
    for attr in attributes:
        if attr.get("id") == key:
            return attr.get("value_name", None)
    return None


def create_tables(file):

    products, sellers, shipments = [], [], []

    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for elem in data:
        attributes = elem.get("attributes", []) 

        # Productos
        products.append({
            "product_id": elem["id"],
            "seller_id": elem["seller"]["id"],
            "title": elem["title"],
            "price": elem["price"],
            "available_quantity": elem["available_quantity"],
            "condition": elem["condition"],
            "brand": get_attribute_value(attributes, "BRAND"),
            "model": get_attribute_value(attributes, "MODEL")
        })
    
        # Vendedores
        sellers.append({
            "seller_id": elem["seller"]["id"],
            "name": elem["seller"]["nickname"],
            "state": elem["address"]["state_name"],
            "city": elem["address"]["city_name"]
        })

        # Envíos
        shipments.append({
            "shipping_id": str(uuid.uuid4()),
            "product_id": elem["id"],
            "store_pick_up": elem["shipping"]["store_pick_up"],
            "free_shipping": elem["shipping"]["free_shipping"],
            "logistic_type": elem["shipping"]["logistic_type"]
        })

    tables = {"products": products, "sellers": sellers, "shipments": shipments}
    for name, data in tables.items():
        load_data(data, f"{name}.json", "processed")