from config import API_BASE_URL, API_TOKEN
import requests
import logging

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