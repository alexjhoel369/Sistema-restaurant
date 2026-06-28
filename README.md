Aquí tienes el **README.md actualizado** con todo lo que implementamos:

---

# 🍽️ Sistema Web de Gestión Integral para Restaurantes

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)

## 📋 Descripción

Plataforma web completa para la gestión integral de restaurantes. Permite administrar comandas, inventario con Kardex, facturación (normativa SIAT Bolivia), control de caja y gestión de usuarios con roles diferenciados.

## ✨ Características Principales

- 🔐 **Autenticación y Autorización** - 5 roles con permisos diferenciados
- 📋 **Gestión de Comandas** - Ciclo completo desde pedido hasta entrega
- 🍳 **Panel de Cocina** - Control de preparación en tiempo real
- 💰 **Facturación** - Emisión de facturas con dosificación SIAT
- 💵 **Control de Caja** - Apertura/cierre con arqueo
- 📦 **Inventario Kardex** - Control de entradas, salidas y ajustes
- 📊 **Dashboard por Rol** - Vistas personalizadas según perfil
- 📝 **Auditoría** - Registro de todas las acciones del sistema

## 👥 Roles del Sistema

| Rol | ID | Funciones |
|-----|----|-----------|
| 🔴 Administrador | 1 | Acceso total al sistema (14 módulos) |
| 🔵 Mesero | 4 | Crear comandas, ver menú |
| 🟣 Cocinero | 5 | Gestionar preparación, ver recetas |
| 🟢 Cajero | 3 | Abrir/cerrar caja, facturar |
| ⚪ Almacenero | 6 | Control de inventario, Kardex |

## 🛠️ Tecnologías

### Backend
- **Python** 3.11+
- **Flask** 2.3+ (Framework web)
- **SQLAlchemy** 2.0+ (ORM)
- **Flask-Login** (Autenticación)
- **Werkzeug** (Hash de contraseñas pbkdf2:sha256)

### Frontend
- **HTML5** + **CSS3**
- **Bootstrap** 5.3 (Diseño responsive)
- **Bootstrap Icons** (Iconografía)
- **JavaScript** (Vanilla)

### Base de Datos
- **PostgreSQL** 15+ (Producción)
- **SQLite** 3 (Desarrollo)

## 📋 Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 15 o superior (opcional, puede usar SQLite)
- pip (gestor de paquetes Python)
- Git

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/alexjhoel369/Sistema-restaurant.git
cd Sistema-restaurant

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Activar en Windows:
venv\Scripts\activate

# Activar en Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
# Editar config.py y establecer tu conexión:
# PostgreSQL: postgresql://usuario:contraseña@localhost:5432/restaurante_db
# SQLite: sqlite:///restaurante.db

# 5. Iniciar servidor
python run.py

# 6. Acceder al sistema
# URL: http://127.0.0.1:5000
```

## 📁 Estructura del Proyecto

```
restaurante_app/
├── app/
│   ├── __init__.py              # Inicialización Flask
│   ├── models/                  # 24 Modelos SQLAlchemy
│   │   ├── rol.py
│   │   ├── usuario.py
│   │   ├── cliente.py
│   │   ├── mesa.py
│   │   ├── producto.py
│   │   ├── insumo.py
│   │   ├── receta.py
│   │   ├── comanda.py
│   │   ├── detalle_comanda.py
│   │   ├── factura.py
│   │   ├── caja_sesion.py
│   │   ├── inventario_movimiento.py
│   │   └── ...
│   ├── services/                # 21 Servicios (lógica de negocio)
│   │   ├── usuario_service.py
│   │   ├── comanda_service.py
│   │   ├── factura_service.py
│   │   ├── inventario_movimiento_service.py
│   │   └── ...
│   ├── routes/                  # 18 Blueprints (controladores)
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   ├── mesero_routes.py
│   │   ├── cocinero_routes.py
│   │   ├── cajero_routes.py
│   │   ├── almacenero_routes.py
│   │   └── ...
│   └── utils/
│       └── decorators.py        # Decoradores de seguridad
├── templates/                   # Plantillas HTML
│   ├── base.html               # Plantilla base
│   ├── auth/
│   │   └── login.html          # Inicio de sesión
│   ├── admin/                  # Vistas del administrador
│   │   ├── dashboard.html
│   │   ├── usuarios.html
│   │   ├── productos.html
│   │   └── ...
│   ├── mesero/                 # Vistas del mesero
│   │   ├── dashboard.html
│   │   ├── crear_comanda.html
│   │   └── ver_comanda.html
│   ├── cocinero/               # Vistas del cocinero
│   │   └── dashboard.html
│   ├── cajero/                 # Vistas del cajero
│   │   ├── dashboard.html
│   │   └── facturar.html
│   └── almacenero/             # Vistas del almacenero
│       ├── dashboard.html
│       └── kardex.html
├── config.py                   # Configuración
├── run.py                      # Punto de entrada
├── requirements.txt            # Dependencias
└── README.md                   # Documentación
```

## 🗄️ Base de Datos

### Tablas Principales (24 total)

| Categoría | Tablas |
|-----------|--------|
| Acceso | `rol`, `usuario` |
| Clientes | `cliente` |
| Mesas | `mesa`, `reserva` |
| Menú | `categoria_producto`, `producto`, `receta` |
| Inventario | `proveedor`, `categoria_insumo`, `insumo`, `inventario_movimiento` |
| Atención | `turno_mesero`, `comanda`, `detalle_comanda` |
| Caja | `metodo_pago`, `caja_sesion`, `caja_arqueo` |
| Facturación | `dosificacion`, `factura`, `factura_pago`, `factura_detalle` |
| Sistema | `configuracion`, `log_auditoria` |

### Datos Iniciales (Seeds)

```sql
-- Roles del sistema
INSERT INTO rol (nombre, descripcion) VALUES
('Administrador', 'Acceso total al sistema'),
('Gerente', 'Gestión administrativa y reportes'),
('Cajero', 'Manejo de caja y facturación'),
('Mesero', 'Atención de mesas y comandas'),
('Cocinero', 'Gestión de preparación de platos'),
('Almacenero', 'Control de inventario e insumos');

-- Métodos de pago
INSERT INTO metodo_pago (codigo, nombre) VALUES
('EFECTIVO', 'Efectivo'),
('TARJETA_CREDITO', 'Tarjeta de Crédito'),
('TARJETA_DEBITO', 'Tarjeta de Débito'),
('QR', 'Código QR'),
('TRANSFERENCIA', 'Transferencia Bancaria');

-- Categorías de productos
INSERT INTO categoria_producto (nombre, descripcion) VALUES
('Entradas', 'Platos de entrada'),
('Platos Fuertes', 'Platos principales'),
('Bebidas', 'Bebidas alcohólicas y no alcohólicas'),
('Postres', 'Postres y dulces'),
('Especialidades', 'Platos especiales de la casa');

-- Categorías de insumos
INSERT INTO categoria_insumo (nombre, descripcion) VALUES
('Carnes', 'Carnes rojas y blancas'),
('Lácteos', 'Productos lácteos'),
('Verduras', 'Verduras y hortalizas'),
('Bebidas', 'Bebidas y licores'),
('Abarrotes', 'Productos secos y enlatados'),
('Limpieza', 'Artículos de limpieza');

-- Usuario administrador (contraseña: admin123)
INSERT INTO usuario (nombre, apellido, email, contraseña_hash, id_rol) VALUES
('Admin', 'Sistema', 'admin@restaurante.com', 
 'pbkdf2:sha256:...', 1);
```

## 🔑 Credenciales por Defecto

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Administrador | admin@restaurante.com | admin123 |

> ⚠️ **Importante:** Cambiar contraseñas en producción

## 🔐 Seguridad

- **Contraseñas:** Hash `pbkdf2:sha256` (werkzeug)
- **Autenticación:** Flask-Login con sesiones protegidas
- **Autorización:** Decoradores por rol
- **SQL Injection:** Prevenido con SQLAlchemy ORM
- **XSS:** Jinja2 auto-escaping
- **CSRF:** Protección en formularios POST

## 🧪 Pruebas Realizadas

| Tipo | Descripción | Estado |
|------|------------|--------|
| Unitarias | Services y validaciones | ✅ |
| Integración | Flujo completo por rol | ✅ |
| Caja Negra | Formularios y validaciones | ✅ |
| Estrés | 50 peticiones simultáneas | ✅ |
| Seguridad | SQL Injection, XSS, acceso no autorizado | ✅ |

## 📊 Módulos Funcionales

### Administrador (14 módulos)
- Dashboard, Usuarios, Roles, Clientes, Mesas
- Categorías Productos, Productos, Recetas
- Proveedores, Categorías Insumos, Insumos
- Movimientos Inventario, Configuración, Auditoría

### Mesero (4 módulos)
- Dashboard, Nueva Comanda, Mis Comandas, Ver Menú

### Cocinero (2 módulos)
- Panel de Preparación, Ver Recetas

### Cajero (3 módulos)
- Caja, Facturación, Clientes

### Almacenero (2 módulos)
- Dashboard Inventario, Kardex

## 🔄 Flujo de Trabajo

```
1. Admin → Configura productos, mesas, insumos, usuarios
2. Mesero → Inicia turno → Crea comanda → Agrega productos
3. Cocinero → Ve pendientes → Prepara → Marca listo
4. Mesero → Entrega → Cierra comanda
5. Cajero → Abre caja → Factura → Cobra → Cierra caja
6. Almacenero → Controla stock → Registra movimientos → Revisa Kardex
```

## 🛠️ Comandos Útiles

```bash
# Iniciar servidor desarrollo
python run.py

# Crear usuario administrador
python create_admin.py

# Crear dosificación para facturación
python crear_dosificacion.py

# Reparar contraseñas
python fix_passwords.py

# Acceder a Flask shell
flask shell
```

## 📝 Mantenimiento

### Backup de Base de Datos
```bash
pg_dump -U postgres restaurante_db > backup_$(date +%Y%m%d).sql
```

### Restaurar Base de Datos
```bash
psql -U postgres restaurante_db < backup_20260101.sql
```

### Limpiar Logs Antiguos (> 90 días)
```python
from app.services.log_auditoria_service import LogAuditoriaService
LogAuditoriaService.limpiar_antiguos(90)
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Alex Jhoel**  
GitHub: [@alexjhoel369](https://github.com/alexjhoel369)

## 🙏 Agradecimientos

- Flask y SQLAlchemy por el excelente framework
- Bootstrap por el sistema de diseño
- PostgreSQL por la robusta base de datos

---

**Versión:** 2.0.0  
**Última actualización:** Junio 2026  
**Estado:** ✅ Funcional - 5 roles implementados