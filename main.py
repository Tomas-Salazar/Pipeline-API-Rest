import logging
import requests
import time

from config import API_BASE_URL, API_TOKEN

from requests.exceptions import RequestException, HTTPError, Timeout


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

def obtener_data(dataset_type:str = 'ecommerce', rows:int = 1000) -> dict:
    '''Obtiene datos desde la API'''
    url = f'{API_BASE_URL}/datasets.php'
    params = {
        'type': dataset_type,
        'rows': rows,
        'token': API_TOKEN
    }
    
    logger.info(f'Obteniendo {rows} filas del dataset {dataset_type} desde la API')
    
    response = requests.get(url=url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    logger.info(f'Se recibió {len(data)} registros desde la API')
    
    return data

def obtener_data_con_reintentos(
    dataset_type:str = 'ecommerce',
    rows:int = 1000,
    max_retries:int = 3,
    backoff_factor:float = 2.0  # Factor de espera exponencial entre reintentos
    ) -> dict:
    '''Obtiene datos con reintentos automáticos'''
    for attempt in range(max_retries):
        try:
            return obtener_data(dataset_type, rows)
        except Timeout:
            logger.warning(f"Timeout en intento {attempt + 1}/{max_retries}")
        except HTTPError as e:
            if e.response.status_code >= 500:
                logger.warning(f"Error del servidor: {e}")
            else:
                logger.error(f"Error del cliente: {e}")
                raise   # Errores 4xx no se reintentan
        except RequestException as e:
            logger.warning(f"Error de conexión: {e}")

        if attempt < max_retries - 1:
            wait_time = backoff_factor ** attempt
            logger.info(f"Reintentando en {wait_time} segundos...")
            time.sleep(wait_time)
    
    raise Exception(f"No se pudo obtener datos después de {max_retries} intentos")

data = obtener_data_con_reintentos()
print(data)