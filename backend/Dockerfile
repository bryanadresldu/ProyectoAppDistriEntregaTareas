# Imagen base ligera de Python
FROM python:3.11-slim

WORKDIR /app

# Copiamos primero los requirements para aprovechar la cache de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del codigo fuente
COPY src ./src

# Puerto interno en el que escucha Flask (no se expone al host, solo a la
# red interna). Se mantiene 3000 -- igual que el backend Node anterior --
# para que nginx/nginx.conf y docker-compose.yml no necesiten cambios.
EXPOSE 3000

# Usuario no root por buenas practicas de seguridad
RUN useradd -m appuser
USER appuser

CMD ["python", "src/app.py"]
