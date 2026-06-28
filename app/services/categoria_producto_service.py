from app import db
from app.models.categoria_producto import CategoriaProducto
from sqlalchemy.exc import IntegrityError

class CategoriaProductoService:
    
    @staticmethod
    def listar():
        return CategoriaProducto.query.order_by(CategoriaProducto.nombre).all()

    @staticmethod
    def listar_activas():
        return CategoriaProducto.query.filter_by(activo=True).order_by(CategoriaProducto.nombre).all()

    @staticmethod
    def obtener(id_categoria):
        return db.session.get(CategoriaProducto, id_categoria)

    @staticmethod
    def crear(nombre, descripcion=None):
        if not nombre or not nombre.strip():
            return False, "Error: El nombre de la categoría no puede estar vacío."
        
        try:
            categoria = CategoriaProducto(
                nombre=nombre.strip().capitalize(),
                descripcion=descripcion.strip() if descripcion else None
            )
            db.session.add(categoria)
            db.session.commit()
            return True, "Categoría creada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe una categoría con ese nombre."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear categoría: {str(e)}"

    @staticmethod
    def actualizar(id_categoria, nombre, descripcion=None, activo=True):
        try:
            categoria = db.session.get(CategoriaProducto, id_categoria)
            if not categoria:
                return False, "Categoría no encontrada."

            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."

            # Validar duplicados si cambió el nombre
            if categoria.nombre != nombre.strip().capitalize():
                if CategoriaProducto.query.filter_by(nombre=nombre.strip().capitalize()).first():
                    return False, "Error: Ya existe otra categoría con ese nombre."

            categoria.nombre = nombre.strip().capitalize()
            categoria.descripcion = descripcion.strip() if descripcion else None
            categoria.activo = activo

            db.session.commit()
            return True, "Categoría actualizada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otra categoría con ese nombre."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar categoría: {str(e)}"

    @staticmethod
    def eliminar(id_categoria):
        try:
            categoria = db.session.get(CategoriaProducto, id_categoria)
            if not categoria:
                return False, "Categoría no encontrada."

            db.session.delete(categoria)
            db.session.commit()
            return True, "Categoría eliminada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar la categoría porque tiene productos asociados."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"