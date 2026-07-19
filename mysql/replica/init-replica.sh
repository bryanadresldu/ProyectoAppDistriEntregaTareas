#!/bin/bash
# =============================================================
# Se ejecuta automaticamente SOLO en el primer arranque del
# contenedor (docker-entrypoint-initdb.d), cuando el volumen de
# datos de la replica esta vacio.
#
# No crea el esquema manualmente: la replica lo obtiene completo
# (tablas + datos semilla) reproduciendo el binary log del Master
# desde el inicio, gracias a SOURCE_AUTO_POSITION=1 (GTID).
#
# Objetivo: que el usuario NO tenga que ejecutar comandos manuales
# para dejar la replicacion funcionando.
# =============================================================
set -e

echo "[replica-init] Configurando replicacion hacia mysql-master..."

mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<-EOSQL
  CHANGE REPLICATION SOURCE TO
    SOURCE_HOST = 'mysql-master',
    SOURCE_PORT = 3306,
    SOURCE_USER = 'replicator',
    SOURCE_PASSWORD = 'ReplicaPass123!',
    SOURCE_AUTO_POSITION = 1,
    GET_SOURCE_PUBLIC_KEY = 1;

  START REPLICA;
EOSQL

echo "[replica-init] Replicacion configurada e iniciada."
