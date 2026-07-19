-- =============================================================
-- Inicializacion de la base de datos en el MySQL MASTER
-- Se ejecuta automaticamente una sola vez (primer arranque del
-- contenedor) porque este script vive en /docker-entrypoint-initdb.d
-- =============================================================

CREATE DATABASE IF NOT EXISTS tareas_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE tareas_db;

-- ---------------------------------------------------------
-- Tabla: usuarios
-- ---------------------------------------------------------
-- El rol determina los permisos: 'student' consulta y entrega tareas;
-- 'teacher' (docente) puede registrar nuevas tareas en el sistema.
CREATE TABLE IF NOT EXISTS usuarios (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  nombre_completo  VARCHAR(150) NOT NULL,
  correo           VARCHAR(150) NOT NULL UNIQUE,
  contrasena_hash  VARCHAR(255) NOT NULL,
  rol              ENUM('student', 'teacher') NOT NULL DEFAULT 'student',
  creado_en        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Tabla: tareas
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS tareas (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  titulo        VARCHAR(200) NOT NULL,
  codigo        VARCHAR(50)  NOT NULL UNIQUE,
  descripcion   TEXT NOT NULL,
  fecha_limite  DATETIME NOT NULL,
  creado_por    INT NULL,
  creado_en     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_tareas_creado_por FOREIGN KEY (creado_por) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Tabla: entregas
-- Un estudiante NO puede entregar dos veces la misma tarea:
-- se garantiza con la restriccion UNIQUE(estudiante_id, tarea_id).
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS entregas (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  estudiante_id INT NOT NULL,
  tarea_id      INT NOT NULL,
  respuesta     TEXT NOT NULL,
  entregado_en  DATETIME NOT NULL,
  CONSTRAINT fk_entregas_estudiante FOREIGN KEY (estudiante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  CONSTRAINT fk_entregas_tarea FOREIGN KEY (tarea_id) REFERENCES tareas(id) ON DELETE CASCADE,
  CONSTRAINT uq_entrega_estudiante_tarea UNIQUE (estudiante_id, tarea_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Usuario de replicacion (solo con privilegio de REPLICATION SLAVE)
-- La Replica se conecta al Master usando este usuario.
-- ---------------------------------------------------------
CREATE USER IF NOT EXISTS 'replicator'@'%' IDENTIFIED BY 'ReplicaPass123!';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
FLUSH PRIVILEGES;

-- ---------------------------------------------------------
-- Datos de prueba: estudiantes
-- Contrasena en texto plano para TODOS: Estudiante123!
-- (hash generado con bcryptjs, factor de costo 10)
-- ---------------------------------------------------------
INSERT INTO usuarios (nombre_completo, correo, contrasena_hash, rol) VALUES
  ('Ana Torres',   'ana.torres@epn.edu.ec',   '$2b$10$SB87yRHFyTqkZhYMBmXka.47QgFf6sEq7teoIuAMl6ChJEpCAFsS6', 'student'),
  ('Luis Andrade', 'luis.andrade@epn.edu.ec', '$2b$10$og0nbtbR4j1Zn2tQSKy/G.pLVVJl1NdBfzcCsFd1WKiz5DZifqX7W', 'student'),
  ('Maria Chasi',  'maria.chasi@epn.edu.ec',  '$2b$10$SXQ5jyyN3ZwieUSWbtj18OdV66ezflihhZlxZoaCYC50Oq70mazZq', 'student');

-- ---------------------------------------------------------
-- Datos de prueba: docente
-- Contrasena en texto plano: Docente123!
-- ---------------------------------------------------------
INSERT INTO usuarios (nombre_completo, correo, contrasena_hash, rol) VALUES
  ('Vanessa Guevara', 'vanessa.guevara@epn.edu.ec', '$2b$10$EK1rk.xWEoM7y77fcyvUCO8L0xvDQLr6zhRgfle9tyBp3bVuSCd72', 'teacher');

-- ---------------------------------------------------------
-- Datos de prueba: tareas
-- Se asocian al docente semilla (subquery por email, para no
-- depender de que su id autoincremental sea siempre el mismo).
-- ---------------------------------------------------------
INSERT INTO tareas (titulo, codigo, descripcion, fecha_limite, creado_por) VALUES
  ('Fundamentos de Contenedores Docker', 'AD-T01',
   'Investigar y explicar los conceptos de imagen, contenedor y volumen en Docker. Entregar un resumen de al menos 300 palabras.',
   DATE_ADD(NOW(), INTERVAL 10 DAY),
   (SELECT id FROM usuarios WHERE correo = 'vanessa.guevara@epn.edu.ec')),

  ('Arquitectura Cliente-Servidor Distribuida', 'AD-T02',
   'Describir con un diagrama y texto explicativo la arquitectura cliente-servidor aplicada a sistemas distribuidos modernos.',
   DATE_ADD(NOW(), INTERVAL 15 DAY),
   (SELECT id FROM usuarios WHERE correo = 'vanessa.guevara@epn.edu.ec')),

  ('Balanceo de Carga con NGINX', 'AD-T03',
   'Explicar las diferencias entre balanceo por round-robin, por pesos y por menor numero de conexiones. Incluir ejemplos.',
   DATE_ADD(NOW(), INTERVAL 20 DAY),
   (SELECT id FROM usuarios WHERE correo = 'vanessa.guevara@epn.edu.ec')),

  ('Replicacion de Bases de Datos', 'AD-T04',
   'Redactar un informe sobre replicacion Master/Replica en MySQL: ventajas, desventajas y casos de uso reales.',
   DATE_ADD(NOW(), INTERVAL 25 DAY),
   (SELECT id FROM usuarios WHERE correo = 'vanessa.guevara@epn.edu.ec')),

  ('Pruebas de Carga con k6', 'AD-T05',
   'Disenar un plan de pruebas de carga para un sistema web distribuido, identificando metricas clave a monitorear.',
   DATE_ADD(NOW(), INTERVAL 30 DAY),
   (SELECT id FROM usuarios WHERE correo = 'vanessa.guevara@epn.edu.ec')),

  ('Tarea de Practica Ya Vencida', 'AD-T00',
   'Tarea de ejemplo para demostrar el bloqueo de entregas fuera de plazo (su fecha limite ya paso).',
   DATE_SUB(NOW(), INTERVAL 2 DAY),
   (SELECT id FROM usuarios WHERE correo = 'vanessa.guevara@epn.edu.ec'));
