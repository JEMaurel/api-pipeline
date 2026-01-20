import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "https://iansaura.com/api")
API_EMAIL = os.getenv("API_EMAIL")

if not API_TOKEN:
    raise ValueError("API_TOKEN no configurado. crea un archivo .env ")
if not API_EMAIL:
    raise ValueError("API_EMAIL no configurado. crea un archivo .env")
