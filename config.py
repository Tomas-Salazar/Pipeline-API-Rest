import os
from dotenv import load_dotenv

# Credenciales de la API
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")