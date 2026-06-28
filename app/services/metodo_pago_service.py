from app import db
from app.models.metodo_pago import MetodoPago
from sqlalchemy.exc import IntegrityError

class MetodoPagoService:
    
    @staticmethod
    def listar():
        return MetodoPago.query.order_by(MetodoPago.nombre).all()

    @staticmethod
    def listar_activos():
        return MetodoPago.query.filter_by(activo=True).order_by(MetodoPago.nombre).all()

    @staticmethod
    def obtener(id_metodo):
        return db.session.get(MetodoPago, id_metodo)

    @staticmethod
    def obtener_por_codigo(codigo):
        return MetodoPago.query.filter_by(codigo=codigo).first()

    @staticmethod
    def crear(codigo, nombre, requiere_referencia=False):
        if not codigo or not codigo.strip():
            return False, "Error: El código no puede estar vacío."
        if not nombre or not nombre.strip():
            return False, "Error: El nombre no puede estar vacío."
        
        try:
            metodo = MetodoPago(
                codigo=codigo.strip().upper(),
                nombre=nombre.strip().capitalize(),
                requiere_referencia=requiere_referencia
            )
            db.session.add(metodo)
            db.session.commit()
            return True, "Método de pago creado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe un método de pago con ese código."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear método de pago: {str(e)}"

    @staticmethod
    def actualizar(id_metodo, codigo, nombre, requiere_referencia=False, activo=True):
        try:
            metodo = db.session.get(MetodoPago, id_metodo)
            if not metodo:
                return False, "Método de pago no encontrado."

            if not codigo or not codigo.strip():
                return False, "Error: El código no puede estar vacío."
            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."

            # Validar código único si cambió
            if metodo.codigo != codigo.strip().upper():
                if MetodoPago.query.filter_by(codigo=codigo.strip().upper()).first():
                    return False, "Error: Ya existe otro método con ese código."

            metodo.codigo = codigo.strip().upper()
            metodo.nombre = nombre.strip().capitalize()
            metodo.requiere_referencia = requiere_referencia
            metodo.activo = activo

            db.session.commit()
            return True, "Método de pago actualizado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otro método con ese código."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar método de pago: {str(e)}"

    @staticmethod
    def eliminar(id_metodo):
        try:
            metodo = db.session.get(MetodoPago, id_metodo)
            if not metodo:
                return False, "Método de pago no encontrado."

            db.session.delete(metodo)
            db.session.commit()
            return True, "Método de pago eliminado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar el método de pago porque tiene pagos o arqueos asociados."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"