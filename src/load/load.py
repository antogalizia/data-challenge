from pathlib import Path
import json

def load_data(json_data: dict, file_name: str, relative_path: str):
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
        return str(file_path)

    except (OSError, json.JSONDecodeError) as e:
        print(f"Error al guardar el archivo JSON: {e}")
        raise  
    

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
                f.write(json.dumps(obj) + "\n")  # Escribe cada objeto en una nueva línea

    except (OSError, json.JSONDecodeError) as e:
        print(f"Error al guardar el archivo JSON: {e}")
        raise  