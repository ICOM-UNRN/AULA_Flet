-- Creación Base de datos
-- CREATE DATABASE aula_datos

-- Definición del dominio Tnombre
CREATE DOMAIN Tnombre VARCHAR(50) NOT NULL;

-- Definición de la tabla profesor
CREATE TABLE profesor (
  id SERIAL PRIMARY KEY,
  documento INTEGER UNIQUE,
  nombre Tnombre,
  apellido Tnombre,
  condicion Tnombre,
  categoria Tnombre,
  dedicacion Tnombre,
  periodo_a_cargo TEXT
);

-- Definición de la tabla Materia
CREATE TABLE materia (
  id SERIAL PRIMARY KEY,
  codigo_guarani VARCHAR(50) NOT NULL UNIQUE,
  carrera Tnombre,
  nombre Tnombre,
  anio INTEGER,
  cuatrimestre INTEGER,
  taxonomia Tnombre,
  horas_semanales INTEGER,
  comisiones INTEGER
);

-- Definición de la tabla profesor por materia
CREATE TABLE profesor_por_materia(
  id_materia INTEGER REFERENCES materia
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  id_profesor INTEGER REFERENCES profesor
    ON UPDATE CASCADE
    ON DELETE SET NULL,
  alumnos_esperados INTEGER,
  tipo_clase Tnombre,
  activo BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (id_materia, alumnos_esperados, tipo_clase),
  UNIQUE (id_materia, id_profesor, alumnos_esperados, tipo_clase)
);

-- Definición de la tabla Edificio
CREATE TABLE edificio (
  id SERIAL PRIMARY KEY,
  nombre Tnombre,
  calle Tnombre,
  altura INTEGER
);

-- Definición de la tabla Aula
CREATE TABLE aula (
  id_aula SERIAL PRIMARY KEY,
  nombre tnombre NOT NULL,
  id_edificio INTEGER REFERENCES edificio
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

-- Definición de la tabla Evento
CREATE TABLE evento (
  id SERIAL PRIMARY KEY,
  nombre Tnombre,
  descripcion TEXT,
  comienzo DATE,
  fin DATE
);

-- Definición de la tabla Recurso
CREATE TABLE recurso (
  id_recurso SERIAL PRIMARY KEY,
  nombre Tnombre,
  descripcion TEXT
);

-- Definición de la tabla Recurso_por_aula
CREATE TABLE recurso_por_aula (
  id_aula INTEGER REFERENCES aula
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  id_recurso INTEGER REFERENCES recurso
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  cantidad INTEGER,
  PRIMARY KEY (id_aula, id_recurso)
);

-- Definición de la tabla Recurso_por_aula
CREATE TABLE asignacion (
  id SERIAL PRIMARY KEY,
  id_aula INTEGER REFERENCES aula
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  id_materia INTEGER REFERENCES materia
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  id_evento INTEGER REFERENCES evento
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  dia Tnombre NOT NULL CHECK (dia IN ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo')),
  horario_comienzo INTEGER NOT NULL,
  horario_fin INTEGER NOT NULL,
  UNIQUE (id_aula, dia, horario_comienzo)
);

-- Tabla de auditoría
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    log_time TIMESTAMP DEFAULT current_timestamp,
    user_name TEXT,
    database_name TEXT,
    client_addr TEXT,
    operation TEXT,
    table_name TEXT,
    record_id INTEGER,
    old_data JSONB,
    new_data JSONB
);

