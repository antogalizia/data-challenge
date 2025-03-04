from load.load import load_ndjson
import json
import uuid


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
        load_ndjson(data, f"{name}_table.json", "clean")