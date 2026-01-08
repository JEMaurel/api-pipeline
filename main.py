import requests
import time
import logging
from requests.exceptions import RequestException ,Timeout, HTTPError
from config import API_TOKEN, API_BASE_URL, API_EMAIL
from transform import transform_data 

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
def main():
    logger.info("="*50)
    logger.info("iniciando la recuperacion de datos  paso 6 extraction + retry")
    logger.info("="*50)
    data = fetch_data_with_retry(rows=1000)
    df= transform_data(data)
    if df.empty:
        logger.error("no hay datos transformados . abortando pipeline")
        return
    logger.info(f"transformacion exitosa")

    logger.info("pipeline ejecutado correctamente")


if __name__ == "__main__":
    main()
    
