import os
from dotenv import load_dotenv

# En Docker las variables ya vienen inyectadas por docker-compose.yml;
# load_dotenv() es un no-op inofensivo si no encuentra un archivo .env
# (util solo para ejecutar el backend fuera de un contenedor).
load_dotenv()


def _required(name):
    value = os.environ.get(name)
    if value is None or value == '':
        raise RuntimeError(f'Falta la variable de entorno obligatoria: {name}')
    return value


PORT = int(os.environ.get('PORT', 3000))
APP_NODE_NAME = os.environ.get('APP_NODE_NAME', 'app-node-unknown')

DB_HOST = _required('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_USER = _required('DB_USER')
DB_PASSWORD = _required('DB_PASSWORD')
DB_NAME = _required('DB_NAME')

JWT_SECRET = _required('JWT_SECRET')
JWT_EXPIRES_IN = os.environ.get('JWT_EXPIRES_IN', '2h')
