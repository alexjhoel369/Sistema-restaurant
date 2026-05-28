# Sistema-restaurant
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