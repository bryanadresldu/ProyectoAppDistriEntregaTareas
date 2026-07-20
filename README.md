# Sistema de Gestión de Tareas — Aplicación Distribuida

Proyecto final de **Aplicaciones Distribuidas** — Escuela Politécnica Nacional.
Aplicación web para que estudiantes consulten tareas y entreguen sus respuestas,
desplegada sobre una arquitectura distribuida real con Docker: balanceo de carga
con NGINX, tres nodos de aplicación idénticos y replicación MySQL Master/Replica.

## 🚀 Arquitectura Básica
```
Navegador (http://localhost)
        │
        ▼
     NGINX  ── balanceo de carga por PESOS (weighted round-robin)
        │
   ┌────┼────┐
   ▼    ▼    ▼
 node-1 node-2 node-3      (misma imagen Python + Flask, stateless)
   │    │    │
   └────┼────┘
        ▼
  MySQL MASTER  (todas las escrituras)  ◄──── phpMyAdmin (http://localhost:8081)
        │                                     ◄──── cliente MySQL en Windows (localhost:3306)
        ▼  replicación binlog + GTID
  MySQL REPLICA (solo lectura / respaldo distribuido)  ◄──── cliente MySQL en Windows (localhost:3307)
                                                        ◄──── phpMyAdmin (login manual)
```
- **Frontend & Balanceador:** NGINX
- **Backend:** 3 nodos idénticos (Python + Flask) stateless
- **Base de Datos:** MySQL 8.0 (1 Master para escrituras, 1 Replica para lecturas) + phpMyAdmin

## ⚙️ Requisitos
- **Docker Desktop** instalado y en ejecución.
- Haber creado el archivo `.env` (puedes copiar el contenido de `.env.example`).

## 🏃‍♂️ Cómo ejecutar
Desde la terminal en la raíz del proyecto, ejecuta:
```bash
docker compose up --build
```
*(Espera a que todos los contenedores aparezcan como "healthy")*

## 🌐 Accesos
- **Aplicación Web:** http://localhost
- **phpMyAdmin (BD):** http://localhost:8081

## 🔑 Credenciales de Prueba

| Correo                          | Contraseña        | Rol        |
|-----------------------------------|--------------------|------------|
| ana.torres@epn.edu.ec            | `Estudiante123!`   | Estudiante |
| luis.andrade@epn.edu.ec          | `Estudiante123!`   | Estudiante |
| maria.chasi@epn.edu.ec           | `Estudiante123!`   | Estudiante |
| vanessa.guevara@epn.edu.ec       | `Docente123!`      | Docente    |

Las contraseñas se almacenan como hash `bcrypt` (nunca en texto plano) en la
tabla `usuarios`. El campo `rol` determina qué puede hacer cada cuenta:

- **Estudiante**: consulta tareas y las entrega (una sola vez por tarea).
- **Docente**: consulta tareas y **registra tareas nuevas** desde un panel
  dedicado (`Panel docente` en el menú, tras iniciar sesión). No puede
  entregar tareas — esa acción está reservada a estudiantes tanto en el
  frontend como en el backend (`requireRole('student')` en las rutas de
  entrega).

## 🛑 Comandos Útiles

```bash
# Detener sin borrar los datos de la base de datos
docker compose stop

# Detener y eliminar los contenedores y la red
docker compose down

# Reinicio total (borra contenedores y los datos de MySQL)
docker compose down -v
```
