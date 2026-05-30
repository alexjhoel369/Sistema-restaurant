# Sistema Web de Gestión Integral para Restaurantes - version

## Descripción
Plataforma web para gestión de comandas, inventario, facturación y reportes en restaurantes.

## Tecnologías
- Backend: Python 3.11 + Flask 2.3.2
- Frontend: HTML5 + CSS3 + Bootstrap 5 + JavaScript
- Base de Datos: PostgreSQL 15.x
- ORM: SQLAlchemy 2.0.19
- Autenticación: JWT + bcrypt

## Requisitos Previos
- Python 3.11+
- PostgreSQL 15+
- pip (gestor de paquetes Python)

## Instalación Rápida
1. Clonar repositorio: `git clone https://github.com/alexjhoel369/Sistema-restaurant.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Iniciar servidor: `python run.py`

## Estructura del Proyecto

Sistema Web de Gestión Integral para Restaurantes 

# Para iniciar 
Sistema-restaurant> python run.py

# config BD
Datos iniciales para BD "restaurante" con ese nombre se crea la BD

# usas  estas consultas para iniciar desde el login o puedes acceder
# directamente a las rutas desde navegador.
DATOS INICIALES (SEED)
-- =========================================

-- ROLES
INSERT INTO rol (nombre) VALUES
('admin'),
('mesero');

-- USUARIO ADMIN
INSERT INTO usuario (nombre, email, contraseña_hash, id_rol)
VALUES ('Admin', 'admin@test.com', '123456', 1);

-- MESAS
INSERT INTO mesa (numero, capacidad) VALUES
(1, 4),
(2, 4),
(3, 2);

-- CATEGORÍAS
INSERT INTO categoria_producto (nombre) VALUES
('Platos'),
('Bebidas');

-- PRODUCTOS
INSERT INTO producto (nombre, precio, id_categoria) VALUES
('Hamburguesa', 25.00, 1),
('Pizza', 40.00, 1),
('Coca-Cola', 8.00, 2);

-- PROVEEDORES
INSERT INTO proveedor (nombre, telefono) VALUES
('Proveedor Local', '77777777');

-- INVENTARIO
INSERT INTO inventario (id_producto, stock_actual, stock_minimo) VALUES
(1, 50, 10),
(2, 40, 10),
(3, 100, 20);

-- =========================================
-- FIN DEL SCRIPT
-- =========================================