
# Pipeline ETL + API con FastAPI 

## Descripción

Este proyecto implementa un pipeline ETL que extrae, transforma y limpia datos provistos por una API pública de Mercado Libre, almacenándolos en las diferentes etapas dentro de la estructura de directorios `raw`, `processed` y `clean`. De manera subyacente, se utiliza FastAPI para exponer los datos mediante una API que se encuentra desplegada en Render.

## Estructura del Proyecto

```
├── src/                
│   ├── etl.py         # Código fuente del pipeline: clases Extract, Transform, Load
│   ├── init.sql       # Script SQL para crear tablas en BigQuery
│
├── data/              # Datos de entrada y salida (cache)
│   ├── raw/           # Datos sin procesar (extraídos)
│   ├── processed/     # Datos parseados
│   ├── clean/         # Datos limpios
│
├── app/               # Construcción de la API con FastAPI
│   ├── main.py        # Punto de entrada de la API
│   ├── routes.py      # Definición de endpoints
│   ├── services.py    # Funciones que invocan los métodos de las clases
│
├── render.yaml        # Configuración para despliegue
├── requirements.txt   # Dependencias del proyecto
├── .gitignore         # Archivos a ignorar por Git (incluye `data/`)
├── README.md          # Documentación del proyecto
```


## 🔧 Despliegue en Render  

La API está disponible en:  
🔗 [https://data-challenge.onrender.com](https://data-challenge.onrender.com)  

### Endpoints Disponibles

- **Obtener datos extraídos:**
  ```sh
  curl -X GET "https://data-challenge.onrender.com/extraction"
  ```
- **Obtener datos transformados:**
  ```sh
  curl -X GET "https://data-challenge.onrender.com/processed"
  ```

    En particular también se puede acceder a `processed/products`, `processed/shipments` y `processed/sellers` para obtener la información segmentada.
<br>

- **Obtener datos limpios:**
  ```sh
  curl -X GET "https://data-challenge.onrender.com/cleaned"
  ```

  Ídem ítem anterior para acceder a la información segmentada.
<br>

### Instalación y uso local

1. Clonar el repositorio.
   ```sh
   git clone https://github.com/antogalizia/data-challenge.git
   cd data-challenge
   ```
2. Crear y activar un entorno virtual.
   ```sh
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   venv\Scripts\activate     # En Windows
   ```
3. Instalar dependencias.
   ```sh
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor FastAPI:

    ```sh
    uvicorn app.main:app --reload
    ```

***
## Flujo ETL

### Extracción (`get_data()` en `etl.py`)

- La función `get_data()` está diseñada para realizar múltiples solicitudes GET a una API y los datos extraídos son almacenados en `data/raw/` en formato JSON. 
- Se implementa un mecanismo de paginación basado en el parámetro offset, que se actualiza en cada iteración con un incremento de 50 registros (params.update({"offset": i * 50})).

##### Manejo de Errores.
- Se captura cualquier excepción relacionada con la solicitud HTTP usando requests.exceptions.RequestException, lo que permite manejar fallas en la conexión o problemas con el servidor.
- Se utiliza response.raise_for_status() para detectar códigos de error HTTP y lanzar una excepción si la respuesta no es exitosa.
- Se captura json.JSONDecodeError en caso de que la API devuelva una respuesta malformada.
  
### Transformación (`parsed_data()`, `cleaning()` en `etl.py`)

- Se leen los datos crudos de la extracción con `parsed_data()` para filtrar y parsearlos al modelo relacional propuesto en el archivo `init.sql` para luego almacenarlos en `data/processed/`. Luego, en `cleaning()` se aplican algunas reglas de limpieza sobre los datos y se almacenan en `data/clean/`.

##### 📊 Modelo Relacional
##### Entidades.
Las entidades identificadas son Productos, Vendedores y Envíos. Cada una contiene sus propios atributos, entre ellos, sus claves primarias y foráneas según corresponda.
##### Relaciones.
Producto - Vendedor: si bien un mismo producto puede ser vendido por múltiples vendedores, se crean publicaciones independientes para vender el mismo producto. Esto significa que cada publicación tiene su propio *product_id*, aunque el producto físico sea el mismo. Por lo tanto, cada producto es vendido por un único vendedor. 

Vendedor - Producto: un vendedor puede publicar múltiples productos.

Dado que la relación es 1:N, en la tabla de productos (Products) se incluye como clave foránea la clave primaria de la tabla de vendedores (Sellers) denominada *seller_id*.  

Envío - Producto: cada producto (publicación) tiene un único envío asociado con su publicación. 

Producto - Envío: si cada *product_id* corresponde a una publicación única, entonces cada publicación tendrá exactamente un único envío asociado.

En la tabla de envíos (Shipments) se incluye como clave foránea la clave primaria de la tabla de productos (Products) denominada *product_id*. Cada vez que se agregue un nuevo envío en la tabla de envíos, el valor de *product_id* debe coincidir con un *product_id* válido que ya exista en la tabla de productos para  garantizar la integridad referencial.

### Carga (`load_data()` en `etl.py`)

- La función `load_data` es utilizada para almacenar archivos en formato JSON resultantes de las diferentes etapas del pipeline. 

