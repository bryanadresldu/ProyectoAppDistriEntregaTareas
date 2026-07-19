# =================================================================
# Se construye una imagen propia (en vez de montar my.cnf como
# bind-mount desde Windows) porque Docker Desktop en Windows monta
# los archivos con permisos "world-writable", y MySQL por seguridad
# IGNORA POR COMPLETO cualquier archivo de configuracion con esos
# permisos (ver warning "World-writable config file ... is ignored").
# Al copiarlo dentro de la imagen con COPY + chmod, el archivo queda
# con permisos correctos y MySQL si lo aplica (gtid_mode, binlog, etc.)
# =================================================================
FROM mysql:8.0

COPY my.cnf /etc/mysql/conf.d/replica.cnf
RUN chmod 0644 /etc/mysql/conf.d/replica.cnf
