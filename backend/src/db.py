import time

import mysql.connector.pooling
import config

# Pool de conexiones hacia MySQL Master (nunca se conecta a la Replica:
# la app siempre escribe y lee contra el Master; la Replica es respaldo
# distribuido, ver scripts/verify-replication.sh).
#
# Se usa un pool (no una conexion nueva por request) para no degradar el
# rendimiento bajo las pruebas de carga de tests/k6/.
#
# NOTA sobre zonas horarias: no se fuerza ningun "time_zone" de sesion
# aqui a proposito. El servidor MySQL ya esta configurado explicitamente
# en UTC (default-time-zone='+00:00' en mysql/master/my.cnf y
# mysql/replica/my.cnf), asi que el pool simplemente hereda esa zona
# horaria por defecto. El frontend es el unico responsable de convertir
# a la hora local del usuario al mostrar fechas.
_dbconfig = {
    'host': config.DB_HOST,
    'port': config.DB_PORT,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'database': config.DB_NAME,
}


def _create_pool(max_attempts=15, delay_seconds=2):
    """Crea el pool de conexiones con reintentos.

    En el primer arranque de todo el proyecto (volumen de MySQL vacio),
    MySQL corre un "servidor temporal" para ejecutar init.sql y luego lo
    reinicia como servidor definitivo. Durante ese reinicio hay una
    ventana breve en la que el healthcheck de Docker puede marcar a
    mysql-master como "healthy" (respondio el servidor temporal) justo
    antes de que se apague para arrancar el definitivo. Si esta app
    intentara conectarse en ese instante y fallara sin reintentar, todo
    el proceso Flask se caeria al importar este modulo. Reintentar aqui
    evita ese problema sin depender de que el healthcheck sea perfecto.
    """
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return mysql.connector.pooling.MySQLConnectionPool(
                pool_name='tareas_pool',
                pool_size=10,
                **_dbconfig
            )
        except mysql.connector.Error as err:
            last_error = err
            print(
                f'[db] MySQL no disponible todavia (intento {attempt}/{max_attempts}): {err}. '
                f'Reintentando en {delay_seconds}s...'
            )
            time.sleep(delay_seconds)
    raise last_error


_pool = _create_pool()


def get_connection():
    """Toma una conexion del pool. connection.close() la devuelve al pool
    (no la cierra de verdad), gracias a como mysql-connector-python
    implementa las conexiones pooled."""
    return _pool.get_connection()
