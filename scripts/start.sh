#!/bin/bash
echo "Construyendo e iniciando todos los servicios..."
docker compose up --build -d
echo "Listo. Abre http://localhost en tu navegador."
