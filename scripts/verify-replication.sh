#!/bin/bash
# =============================================================
# Verifica que la replicacion MySQL Master -> Replica funcione.
# Uso: bash scripts/verify-replication.sh
# (En Windows 11: ejecutar desde Git Bash o WSL; tambien puede
#  correrse el comando docker equivalente manualmente, ver README)
# =============================================================
set -e

echo "================================================================"
echo " 1) Estado de la replicacion (ejecutado en mysql-replica)"
echo "================================================================"
docker compose exec mysql-replica sh -c \
  'mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SHOW REPLICA STATUS\G"' \
  | grep -E "Replica_IO_Running|Replica_SQL_Running|Seconds_Behind_Source|Last_Error|Source_Host"

echo ""
echo "================================================================"
echo " 2) Prueba funcional: escribir en el Master y leer en la Replica"
echo "================================================================"

echo "-> Insertando una tarea de prueba en MySQL MASTER..."
docker compose exec mysql-master sh -c \
  'mysql -u root -p"$MYSQL_ROOT_PASSWORD" tareas_db -e "
    INSERT INTO tareas (titulo, codigo, descripcion, fecha_limite)
    VALUES (\"Verificacion de Replicacion\", CONCAT(\"REPL-\", UNIX_TIMESTAMP()),
            \"Registro insertado por scripts/verify-replication.sh\", DATE_ADD(NOW(), INTERVAL 1 DAY));
  "'

echo "-> Esperando 3 segundos para que la replica sincronice..."
sleep 3

echo "-> Consultando la ultima tarea en MySQL REPLICA..."
docker compose exec mysql-replica sh -c \
  'mysql -u root -p"$MYSQL_ROOT_PASSWORD" tareas_db -e "
    SELECT id, titulo, codigo, creado_en FROM tareas ORDER BY id DESC LIMIT 1;
  "'

echo ""
echo "Si el registro insertado en el Master aparece arriba, la replicacion funciona correctamente."
