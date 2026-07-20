#!/bin/sh
# =============================================================
# Este script existe porque nginx.conf usa un bloque "upstream" con
# los hostnames de los 3 nodos (app-node-1/2/3). NGINX resuelve esos
# nombres UNA SOLA VEZ, al arrancar (al parsear la configuracion), y
# si en ese momento el nombre no se puede resolver todavia en la red
# de Docker, NGINX falla con "host not found in upstream" y el
# contenedor se cae de inmediato.
#
# Esto casi nunca pasa con "docker compose up" (docker-compose.yml ya
# tiene depends_on con condition: service_healthy para los 3 nodos),
# pero SI puede pasar cuando Docker/el sistema se reinicia: ahi cada
# contenedor arranca segun su "restart policy" propia, sin que nadie
# respete el orden de depends_on. Si nginx arranca antes de que los
# nodos existan en la red, se cae y hay que iniciarlo a mano.
#
# Este script simplemente espera (reintentando) a que los 3 nodos
# respondan en el puerto 3000 antes de arrancar NGINX de verdad.
# =============================================================
set -e

hosts="app-node-1 app-node-2 app-node-3"

echo "[nginx-entrypoint] Esperando a que los nodos de la aplicacion esten disponibles..."

for host in $hosts; do
  until nc -z "$host" 3000 2>/dev/null; do
    echo "[nginx-entrypoint]   -> esperando a $host:3000..."
    sleep 1
  done
  echo "[nginx-entrypoint]   -> $host:3000 OK"
done

echo "[nginx-entrypoint] Todos los nodos responden. Iniciando NGINX..."

exec /docker-entrypoint.sh nginx -g "daemon off;"
