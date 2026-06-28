from app import db
from app.models.mesa import Mesa
from sqlalchemy.exc import IntegrityError

class MesaService:
    
    @staticmethod
    def listar():
        return Mesa.query.order_by(Mesa.numero).all()

    @staticmethod
    def listar_disponibles():
        return Mesa.query.filter_by(estado='disponible', activo=True).order_by(Mesa.numero).all()

    @staticmethod
    def listar_activas():
        return Mesa.query.filter_by(activo=True).order_by(Mesa.numero).all()

    @staticmethod
    def obtener(id_mesa):
        return db.session.get(Mesa, id_mesa)

    @staticmethod
    def obtener_por_numero(numero):
        return Mesa.query.filter_by(numero=numero).first()

    @staticmethod
    def crear(numero, capacidad, ubicacion=None):
        if not numero or not numero.strip():
            return False, "Error: El número de mesa no puede estar vacío."
        if capacidad <= 0:
            return False, "Error: La capacidad debe ser mayor a 0."
        
        try:
            # Validar duplicado
            if Mesa.query.filter_by(numero=numero.strip()).first():
                return False, "Error: Ya existe una mesa con ese número."
            
            mesa = Mesa(
                numero=numero.strip(),
                capacidad=capacidad,
                ubicacion=ubicacion.strip() if ubicacion else None
            )
            db.session.add(mesa)
            db.session.commit()
            return True, "Mesa creada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe una mesa con ese número."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear mesa: {str(e)}"

    @staticmethod
    def actualizar(id_mesa, numero, capacidad, ubicacion=None, activo=True):
        try:
            mesa = db.session.get(Mesa, id_mesa)
            if not mesa:
                return False, "Mesa no encontrada."

            # Validar duplicados de número si cambió
            if mesa.numero != numero.strip():
                if Mesa.query.filter_by(numero=numero.strip()).first():
                    return False, "Error: Ya existe otra mesa con ese número."

            mesa.numero = numero.strip()
            mesa.capacidad = capacidad
            mesa.ubicacion = ubicacion.strip() if ubicacion else None
            mesa.activo = activo

            db.session.commit()
            return True, "Mesa actualizada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otra mesa con ese número."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar mesa: {str(e)}"

    @staticmethod
    def cambiar_estado(id_mesa, nuevo_estado):
        """Cambia el estado de una mesa (disponible, ocupada, reservada, mantenimiento)"""
        estados_validos = ['disponible', 'ocupada', 'reservada', 'mantenimiento']
        
        if nuevo_estado not in estados_validos:
            return False, f"Error: Estado no válido. Debe ser: {', '.join(estados_validos)}"
        
        try:
            mesa = db.session.get(Mesa, id_mesa)
            if not mesa:
                return False, "Mesa no encontrada."
            
            mesa.estado = nuevo_estado
            db.session.commit()
            return True, f"Mesa cambiada a estado '{nuevo_estado}' exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cambiar estado: {str(e)}"

    @staticmethod
    def eliminar(id_mesa):
        try:
            mesa = db.session.get(Mesa, id_mesa)
            if not mesa:
                return False, "Mesa no encontrada."

            db.session.delete(mesa)
            db.session.commit()
            return True, "Mesa eliminada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar la mesa porque tiene comandas o reservas asociadas."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"