from app import db
from app.models.categoria_insumo import CategoriaInsumo
from sqlalchemy.exc import IntegrityError

class CategoriaInsumoService:
    
    @staticmethod
    def listar():
        return CategoriaInsumo.query.order_by(CategoriaInsumo.nombre).all()

    @staticmethod
    def listar_activas():
        return CategoriaInsumo.query.filter_by(activo=True).order_by(CategoriaInsumo.nombre).all()

    @staticmethod
    def obtener(id_categoria):
        return db.session.get(CategoriaInsumo, id_categoria)

    @staticmethod
    def crear(nombre, descripcion=None):
        if not nombre or not nombre.strip():
            return False, "Error: El nombre de la categoría no puede estar vacío."
        
        try:
            categoria = CategoriaInsumo(
                nombre=nombre.strip().capitalize(),
                descripcion=descripcion.strip() if descripcion else None
            )
            db.session.add(categoria)
            db.session.commit()
            return True, "Categoría de insumo creada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe una categoría con ese nombre."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear categoría: {str(e)}"

    @staticmethod
    def actualizar(id_categoria, nombre, descripcion=None, activo=True):
        try:
            categoria = db.session.get(CategoriaInsumo, id_categoria)
            if not categoria:
                return False, "Categoría no encontrada."

            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."

            if categoria.nombre != nombre.strip().capitalize():
                if CategoriaInsumo.query.filter_by(nombre=nombre.strip().capitalize()).first():
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
            categoria = db.session.get(CategoriaInsumo, id_categoria)
            if not categoria:
                return False, "Categoría no encontrada."

            db.session.delete(categoria)
            db.session.commit()
            return True, "Categoría eliminada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar la categoría porque tiene insumos asociados."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"