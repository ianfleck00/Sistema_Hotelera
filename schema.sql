-- ======================
-- BASE DE DATOS HOTEL
-- ======================
DROP DATABASE IF EXISTS hotal_bd;
CREATE DATABASE hotal_bd;
USE hotal_bd;

-- ======================
-- TABLA CLIENTES
-- ======================
DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes (
    id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

-- ======================
-- TABLA HABITACIONES
-- ======================
DROP TABLE IF EXISTS habitaciones;
CREATE TABLE habitaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero VARCHAR(10) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    precio_por_noche DECIMAL(10,2) NOT NULL,
    descripcion VARCHAR(255) DEFAULT ''
);

-- ======================
-- TABLA RESERVAS
-- ======================
DROP TABLE IF EXISTS reservas;
CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    habitacion_id INT NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    total DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id) ON DELETE CASCADE
);

-- ======================
-- TABLA USUARIOS (LOGIN)
-- ======================
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- ======================
-- EJEMPLO DE USUARIO ADMIN
-- ======================
INSERT INTO usuarios (username, password) VALUES ('admin', 'admin123');


