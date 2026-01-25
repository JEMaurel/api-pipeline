
import os 
import boto3
from dotenv import load_dotenv 
import requests
import time
import logging
from requests.exceptions import RequestException ,Timeout, HTTPError
from config import API_TOKEN, API_BASE_URL, API_EMAIL
from transform import transform_data 
from save_data import save_data , limpiar_s3_prefix

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fetch_data(dataset_type: str = 'ecommerce', rows: int = 1000) -> dict:
    url = f"{API_BASE_URL}/datasets.php"
    params = {
        'email': API_EMAIL,
        'key': API_TOKEN,
        'type': dataset_type,
        'rows': rows
    }

    logger.info(f"Fetching {rows} rows of {dataset_type} data...")

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    logger.info("Datos recibidos correctamente")
    logger.info(f"received {len(data.get('tables', {}).get('orders', []))} orders")

    return data
#=============================================
# retry...  manejo de errores 
#=============================================

def fetch_data_with_retry(
        dataset_type: str = 'ecommerce',
        rows: int = 1000,
        max_retries: int =3,
        backoff_factor: float = 2.0
) ->dict:
    for attempt in range(max_retries):
        try:
            return fetch_data(dataset_type,rows)
        except Timeout:
            logger.warning(
                f"Timeout en intento {attempt +1} de {max_retries}...reintentando."
            )
        except HTTPError as e:
            if e.response.status_code >=500:
                logger.warning(f"error del servidor: {e}")
            else:
                logger.error(f"error del cliente: {e}")
                raise
        except RequestException as e:
            logger.warning(f"error de conexion: {e}")
        if attempt < max_retries -1:
            wait_time = backoff_factor ** (attempt +1)
            logger.info(f"reintentando en {wait_time} segundos...")
            time.sleep(wait_time)

    raise Exception(f"fallo despues de {max_retries} intentos")
def upload_folder_to_s3(local_dir: str, s3_prefix: str):
    """Sincroniza la carpeta local con el bucket de S3"""
    load_dotenv() # Asegura que lee el .env
    
    bucket_name = os.getenv('S3_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("❌ Error: La variable S3_BUCKET_NAME no está definida en el archivo .env")
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    limpiar_s3_prefix(s3_client, bucket_name, s3_prefix)
    logger.info(f"Iniciando subida a S3: bucket={bucket_name}, prefijo={s3_prefix}")

    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            # Crear la ruta de S3 (ej: processed/orders/year=2024/...)
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")
            
            try:
                s3_client.upload_file(local_path, bucket_name, s3_path)
                logger.info(f"✅ Subido: {s3_path}")
            except Exception as e:
                logger.error(f"❌ Error subiendo {file}: {e}")

def main():
    logger.info("="*50)
    logger.info("iniciando la recuperacion de datos  paso 6 extraction + retry")
    logger.info("="*50)
    try:

        data = fetch_data_with_retry(rows=1000)
        df= transform_data(data)
        if df.empty:
            logger.error("no hay datos transformados . abortando pipeline")
            return
        logger.info(f"transformacion exitosa")
        save_data(df)

        # =============================================
        # NUEVO: PASO 4 - CARGA A AWS S3
        # =============================================
        logger.info("Iniciando fase de carga a la nube...")
        upload_folder_to_s3('output', 'processed')
        # =============================================

        logger.info("="*50)
        logger.info("pipeline ejecutado correctamente")
        logger.info("="*50)
    except Exception as e:
        logger.error(f" fallo del pipeline en main : {e}") 
        raise
        
    

if __name__ == "__main__":
    main()
    
