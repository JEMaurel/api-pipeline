# API Pipe Docker 🚀

Este proyecto es un pipeline de datos (ETL) completamente dockerizado que extrae información de una API de E-commerce, realiza transformaciones de limpieza y organiza un Data Lake local con particionamiento eficiente.

## 🛠️ Tecnologías utilizadas
* **Python 3.11**: Lógica principal del pipeline.
* **Pandas**: Procesamiento y transformación de datos.
* **Docker & Docker Compose**: Contenerización para asegurar la portabilidad.
* **Parquet**: Formato de almacenamiento optimizado para Big Data.
* **WSL2 (Ubuntu)**: Entorno de ejecución y desarrollo.

## 🏗️ Arquitectura del Proyecto
El pipeline sigue una estructura de **Data Lake** profesional:
1. **Extracción**: Obtención de 1000 registros desde una API REST.
2. **Transformación**: Limpieza de columnas y tipado de datos.
3. **Carga (Storage)**: Los datos se guardan en formato `.parquet` usando un esquema de particionamiento **Hive-style** (`order_year=YYYY/order_month=YYYY-MM`).



## 🚀 Cómo ejecutarlo

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/JEMaurel/api-pipe-docker.git](https://github.com/JEMaurel/api-pipe-docker.git)
   cd api-pipe-docker
Configurar variables de entorno: Crea un archivo .env en la raíz con tus credenciales (puedes usar .env.example como guía):

Plaintext
API_TOKEN=tu_token
AWS_ACCESS_KEY_ID=tu_key
...
Ejecutar con Docker:

Bash
docker compose up --build
📂 Estructura de Salida
Al finalizar, los datos procesados se encuentran en la carpeta output/ organizados por tiempo, lo que permite consultas altamente eficientes.

output/orders/
├── order_year=2024
│   └── order_month=2024-01
│       └── data.parquet
