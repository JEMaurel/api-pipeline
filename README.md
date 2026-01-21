# 🚀 API Ecommerce ETL Pipeline

Este proyecto implementa un flujo robusto de **Extracción, Transformación y Carga (ETL)** diseñado para procesar datos de e-commerce de forma eficiente. El sistema consume información de una API REST, aplica transformaciones con Pandas y persiste los resultados en un formato de alto rendimiento (**Parquet**) con particionamiento físico.



---

## ✨ Características Principales

- **Resiliencia:** Lógica de reintentos (Retry strategy) integrada para manejar fallos temporales de red.
- **Dockerizado:** Entorno 100% reproducible mediante Docker y Docker Compose.
- **Almacenamiento Optimizado:** Uso de formato Parquet que reduce el espacio en disco y acelera las consultas analíticas.
- **Particionamiento Automático:** Organización física de datos por año y mes (`order_year`/`order_month`), optimizada para Data Lakes.
- **Seguridad:** Gestión de credenciales sensibles mediante variables de entorno (`.env`).

---

## 🛠️ Requisitos Previos

- **Docker Desktop** (Recomendado) o **Python 3.11+** instalado localmente.
- Conexión a internet para el consumo de la API.

---

## 🚀 Guía de Inicio Rápido con Docker

La forma más eficiente de ejecutar el pipeline es mediante contenedores:



1. **Configurar el entorno:**
   Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:
   ```env
   API_TOKEN=tu_token_aqui
   API_BASE_URL=[https://iansaura.com/api](https://iansaura.com/api)
   API_EMAIL=tu@email.com

2. Levantar el servicio
Desde tu terminal, ejecuta:

Bash

docker-compose up   

🛠️ Instalación Manual (Local)
Si prefieres trabajar en un entorno local sin utilizar Docker:

Bash

# Clonar el repositorio
git clone [https://github.com/JEMaurel/api-pipeline.git](https://github.com/JEMaurel/api-pipeline.git)
cd api-pipeline

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias y ejecutar
pip install -r requirements.txt
python main.py
📊 Flujo del Pipeline
El proceso se ejecuta en tres etapas lógicas:

Extract: Consumo de la API ecommerce con validación de códigos de estado y manejo de excepciones.

Transform: Procesamiento avanzado con Pandas que incluye limpieza de nulos, tipado de datos y normalización.

Load: Escritura en el directorio local /output utilizando el motor PyArrow.

📂 Estructura de Salida (Output)
Los archivos se organizan jerárquicamente para facilitar su consumo en herramientas de BI o motores de SQL:

Plaintext

output/
└── orders/
    ├── order_year=2024/
    │   └── order_month=01/
    │       └── part-0.parquet
    └── order_year=2025/
        └── order_month=01/
            └── part-0.parquet

🧰 Tecnologías Utilizadas
Lenguaje: Python 3.11

Procesamiento de Datos: Pandas

Contenedores: Docker & Docker Compose

Formato de Archivos: Parquet (PyArrow)

Seguridad: Python-dotenv