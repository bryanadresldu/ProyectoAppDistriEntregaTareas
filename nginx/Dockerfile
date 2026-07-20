# NOTA: este Dockerfile se construye con el contexto en la RAIZ del proyecto
# (ver docker-compose.yml: build.context = ".", build.dockerfile = "nginx/Dockerfile")
# para poder copiar tanto la configuracion de nginx como el frontend estatico.

FROM nginx:1.27-alpine

# netcat: usado por docker-entrypoint-wait.sh para comprobar que los
# nodos de la app ya estan disponibles antes de arrancar NGINX.
RUN apk add --no-cache netcat-openbsd

# Configuracion del balanceador de carga (upstream con pesos)
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Frontend estatico (HTML/CSS/JS vanilla) servido directamente por NGINX
COPY frontend /usr/share/nginx/html

# Entrypoint propio: espera a que app-node-1/2/3 respondan en el
# puerto 3000 antes de arrancar NGINX (ver comentarios en el script).
# Evita que NGINX se caiga con "host not found in upstream" cuando
# arranca antes que los nodos, por ejemplo tras reiniciar Docker/el
# sistema (ahi ya no se respeta el depends_on de docker-compose.yml).
COPY nginx/docker-entrypoint-wait.sh /usr/local/bin/docker-entrypoint-wait.sh
RUN chmod +x /usr/local/bin/docker-entrypoint-wait.sh

EXPOSE 80

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-wait.sh"]
