from app import db
from app.models.insumo import Insumo
from app.models.categoria_insumo import CategoriaInsumo
from sqlalchemy.exc import IntegrityError

class InsumoService:
    
    @staticmethod
    def listar():
        return Insumo.query.order_by(Insumo.nombre).all()

    @staticmethod
    def listar_activos():
        return Insumo.query.filter_by(activo=True).order_by(Insumo.nombre).all()

    @staticmethod
    def listar_stock_bajo():
        """Lista insumos con stock por debajo del mínimo"""
        return Insumo.query.filter(
            Insumo.activo == True,
            Insumo.stock_actual <= Insumo.stock_minimo
        ).order_by(Insumo.nombre).all()

    @staticmethod
    def listar_por_categoria(id_categoria):
        return Insumo.query.filter_by(id_categoria=id_categoria, activo=True).order_by(Insumo.nombre).all()

    @staticmethod
    def obtener(id_insumo):
        return db.session.get(Insumo, id_insumo)

    @staticmethod
    def obtener_por_codigo(codigo):
        return Insumo.query.filter_by(codigo=codigo).first()

    @staticmethod
    def buscar(termino):
        """Busca insumos por nombre, código o descripción"""
        return Insumo.query.filter(
            db.or_(
                Insumo.nombre.ilike(f"%{termino}%"),
                Insumo.codigo.ilike(f"%{termino}%"),
                Insumo.descripcion.ilike(f"%{termino}%")
            )
        ).order_by(Insumo.nombre).all()

    @staticmethod
    def crear(codigo, nombre, descripcion, id_categoria, unidad_medida, stock_minimo=10, stock_maximo=100, costo_unitario_promedio=0):
        if not nombre or not nombre.strip():
            return False, "Error: El nombre del insumo no puede estar vacío."
        if stock_minimo < 0:
            return False, "Error: El stock mínimo no puede ser negativo."
        
        try:
            # Validar código único si se proporciona
            if codigo and codigo.strip():
                if Insumo.query.filter_by(codigo=codigo.strip()).first():
                    return False, "Error: Ya existe un insumo con ese código."

            # Validar nombre único
            if Insumo.query.filter_by(nombre=nombre.strip()).first():
                return False, "Error: Ya existe un insumo con ese nombre."

            insumo = Insumo(
                codigo=codigo.strip() if codigo else None,
                nombre=nombre.strip(),
                descripcion=descripcion.strip() if descripcion else None,
                id_categoria=id_categoria,
                unidad_medida=unidad_medida,
                stock_minimo=stock_minimo,
                stock_maximo=stock_maximo,
                costo_unitario_promedio=costo_unitario_promedio
            )
            db.session.add(insumo)
            db.session.commit()
            return True, "Insumo creado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe un insumo con ese código o nombre."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear insumo: {str(e)}"

    @staticmethod
    def actualizar(id_insumo, codigo, nombre, descripcion, id_categoria, unidad_medida, stock_minimo, stock_maximo, costo_unitario_promedio, activo=True):
        try:
            insumo = db.session.get(Insumo, id_insumo)
            if not insumo:
                return False, "Insumo no encontrado."

            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."

            # Validar código único si cambió
            if codigo and codigo.strip() and insumo.codigo != codigo.strip():
                if Insumo.query.filter_by(codigo=codigo.strip()).first():
                    return False, "Error: Ya existe otro insumo con ese código."

            # Validar nombre único si cambió
            if insumo.nombre != nombre.strip():
                if Insumo.query.filter_by(nombre=nombre.strip()).first():
                    return False, "Error: Ya existe otro insumo con ese nombre."

            insumo.codigo = codigo.strip() if codigo else None
            insumo.nombre = nombre.strip()
            insumo.descripcion = descripcion.strip() if descripcion else None
            insumo.id_categoria = id_categoria
            insumo.unidad_medida = unidad_medida
            insumo.stock_minimo = stock_minimo
            insumo.stock_maximo = stock_maximo
            insumo.costo_unitario_promedio = costo_unitario_promedio
            insumo.activo = activo

            db.session.commit()
            return True, "Insumo actualizado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otro insumo con ese código o nombre."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar insumo: {str(e)}"

    @staticmethod
    def eliminar(id_insumo):
        try:
            insumo = db.session.get(Insumo, id_insumo)
            if not insumo:
                return False, "Insumo no encontrado."

            db.session.delete(insumo)
            db.session.commit()
            return True, "Insumo eliminado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar el insumo porque tiene recetas o movimientos asociados."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"