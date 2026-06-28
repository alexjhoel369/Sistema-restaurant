from app import db
from app.models.configuracion import Configuracion
from sqlalchemy.exc import IntegrityError

class ConfiguracionService:
    
    @staticmethod
    def listar():
        return Configuracion.query.order_by(Configuracion.clave).all()

    @staticmethod
    def obtener(id_config):
        return db.session.get(Configuracion, id_config)

    @staticmethod
    def obtener_valor(clave, default=None):
        """Obtiene el valor de una configuración por su clave"""
        config = Configuracion.query.filter_by(clave=clave).first()
        return config.valor if config else default

    @staticmethod
    def obtener_todas_como_dict():
        """Retorna todas las configuraciones como diccionario {clave: valor}"""
        configuraciones = Configuracion.query.all()
        return {config.clave: config.valor for config in configuraciones}

    @staticmethod
    def crear(clave, valor, descripcion=None, tipo='texto', editable=True):
        if not clave or not clave.strip():
            return False, "Error: La clave no puede estar vacía."
        
        try:
            # Validar clave única
            if Configuracion.query.filter_by(clave=clave.strip().lower()).first():
                return False, "Error: Ya existe una configuración con esa clave."

            config = Configuracion(
                clave=clave.strip().lower(),
                valor=str(valor),
                descripcion=descripcion.strip() if descripcion else None,
                tipo=tipo,
                editable=editable
            )
            db.session.add(config)
            db.session.commit()
            return True, "Configuración creada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe una configuración con esa clave."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear configuración: {str(e)}"

    @staticmethod
    def actualizar(id_config, valor, descripcion=None):
        try:
            config = db.session.get(Configuracion, id_config)
            if not config:
                return False, "Configuración no encontrada."

            if not config.editable:
                return False, "Error: Esta configuración no es editable."

            config.valor = str(valor)
            if descripcion:
                config.descripcion = descripcion.strip()

            db.session.commit()
            return True, "Configuración actualizada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar configuración: {str(e)}"

    @staticmethod
    def actualizar_por_clave(clave, valor):
        """Actualiza una configuración por su clave"""
        try:
            config = Configuracion.query.filter_by(clave=clave).first()
            if not config:
                return False, f"Configuración '{clave}' no encontrada."

            if not config.editable:
                return False, "Error: Esta configuración no es editable."

            config.valor = str(valor)
            db.session.commit()
            return True, f"Configuración '{clave}' actualizada."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar: {str(e)}"

    @staticmethod
    def eliminar(id_config):
        try:
            config = db.session.get(Configuracion, id_config)
            if not config:
                return False, "Configuración no encontrada."

            if not config.editable:
                return False, "Error: Esta configuración no se puede eliminar."

            db.session.delete(config)
            db.session.commit()
            return True, "Configuración eliminada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al eliminar configuración: {str(e)}"