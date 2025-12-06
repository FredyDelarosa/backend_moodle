CREATE DATABASE IF NOT EXISTS plataforma_virtual;
USE plataforma_virtual;

CREATE TABLE IF NOT EXISTS programa_estudio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    numero_cuatrimestres INT NOT NULL
);

CREATE TABLE IF NOT EXISTS cuatrimestre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL,
    programa_id INT NOT NULL,
    FOREIGN KEY (programa_id) REFERENCES programa_estudio(id)
);

CREATE TABLE IF NOT EXISTS asignatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    cuatrimestre_id INT NOT NULL,
    codigo VARCHAR(50),
    FOREIGN KEY (cuatrimestre_id) REFERENCES cuatrimestre(id)
);

CREATE TABLE IF NOT EXISTS docente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS docente_asignatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    docente_id INT NOT NULL,
    asignatura_id INT NOT NULL,
    FOREIGN KEY (docente_id) REFERENCES docente(id),
    FOREIGN KEY (asignatura_id) REFERENCES asignatura(id)
);

CREATE TABLE IF NOT EXISTS alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    cuatrimestre INT NOT NULL,
    correo VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS alumno_asignatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    asignatura_id INT NOT NULL,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id),
    FOREIGN KEY (asignatura_id) REFERENCES asignatura(id)
);

CREATE TABLE IF NOT EXISTS grupo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    asignatura_id INT NOT NULL,
    docente_id INT NOT NULL,
    cuatrimestre_id INT NOT NULL,
    capacidad INT NOT NULL DEFAULT 25,
    FOREIGN KEY (asignatura_id) REFERENCES asignatura(id),
    FOREIGN KEY (docente_id) REFERENCES docente(id),
    FOREIGN KEY (cuatrimestre_id) REFERENCES cuatrimestre(id)
);

CREATE TABLE IF NOT EXISTS grupo_alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grupo_id INT NOT NULL,
    alumno_id INT NOT NULL,
    fecha_matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id) REFERENCES grupo(id),
    FOREIGN KEY (alumno_id) REFERENCES alumno(id)
);
