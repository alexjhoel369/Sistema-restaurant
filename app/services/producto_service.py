from app import db
from app.models.producto import Producto
from app.models.categoria_producto import CategoriaProducto
from sqlalchemy.exc import IntegrityError

class ProductoService:
    
    @staticmethod
    def listar():
        return Producto.query.order_by(Producto.nombre).all()

    @staticmethod
    def listar_activos():
        return Producto.query.filter_by(activo=True).order_by(Producto.nombre).all()

    @staticmethod
    def listar_por_categoria(id_categoria):
        return Producto.query.filter_by(id_categoria=id_categoria, activo=True).order_by(Producto.nombre).all()

    @staticmethod
    def obtener(id_producto):
        return db.session.get(Producto, id_producto)

    @staticmethod
    def obtener_por_codigo(codigo):
        return Producto.query.filter_by(codigo=codigo).first()

    @staticmethod
    def buscar(termino):
        """Busca productos por nombre, código o descripción"""
        return Producto.query.filter(
            db.or_(
                Producto.nombre.ilike(f"%{termino}%"),
                Producto.codigo.ilike(f"%{termino}%"),
                Producto.descripcion.ilike(f"%{termino}%")
            )
        ).order_by(Producto.nombre).all()

    @staticmethod
    def crear(codigo, nombre, descripcion, precio, id_categoria, tiempo_preparacion_minutos=15):
        if not nombre or not nombre.strip():
            return False, "Error: El nombre del producto no puede estar vacío."
        if precio < 0:
            return False, "Error: El precio no puede ser negativo."
        
        try:
            # Validar categoría existente
            categoria = db.session.get(CategoriaProducto, id_categoria)
            if not categoria:
                return False, "Error: La categoría seleccionada no existe."

            # Validar código único si se proporciona
            if codigo and codigo.strip():
                if Producto.query.filter_by(codigo=codigo.strip()).first():
                    return False, "Error: Ya existe un producto con ese código."

            producto = Producto(
                codigo=codigo.strip() if codigo else None,
                nombre=nombre.strip(),
                descripcion=descripcion.strip() if descripcion else None,
                precio=precio,
                id_categoria=id_categoria,
                tiempo_preparacion_minutos=tiempo_preparacion_minutos
            )
            db.session.add(producto)
            db.session.commit()
            return True, "Producto creado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe un producto con ese código."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear producto: {str(e)}"

    @staticmethod
    def actualizar(id_producto, codigo, nombre, descripcion, precio, id_categoria, tiempo_preparacion_minutos=15, activo=True):
        try:
            producto = db.session.get(Producto, id_producto)
            if not producto:
                return False, "Producto no encontrado."

            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."
            if precio < 0:
                return False, "Error: El precio no puede ser negativo."

            # Validar código único si cambió
            if codigo and codigo.strip() and producto.codigo != codigo.strip():
                if Producto.query.filter_by(codigo=codigo.strip()).first():
                    return False, "Error: Ya existe otro producto con ese código."

            producto.codigo = codigo.strip() if codigo else None
            producto.nombre = nombre.strip()
            producto.descripcion = descripcion.strip() if descripcion else None
            producto.precio = precio
            producto.id_categoria = id_categoria
            producto.tiempo_preparacion_minutos = tiempo_preparacion_minutos
            producto.activo = activo

            db.session.commit()
            return True, "Producto actualizado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otro producto con ese código."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar producto: {str(e)}"

    @staticmethod
    def eliminar(id_producto):
        try:
            producto = db.session.get(Producto, id_producto)
            if not producto:
                return False, "Producto no encontrado."

            db.session.delete(producto)
            db.session.commit()
            return True, "Producto eliminado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar el producto porque tiene recetas, comandas o facturas asociadas."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"