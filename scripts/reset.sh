#!/bin/bash
echo "ADVERTENCIA: esto elimina contenedores, red Y volumenes (se pierden los datos de MySQL)."
read -p "Escribe 'si' para confirmar: " confirm
if [ "$confirm" = "si" ]; then
  docker compose down -v
  echo "Contenedores y volumenes eliminados."
else
  echo "Operacion cancelada."
fi
