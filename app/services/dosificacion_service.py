from app import db
from app.models.dosificacion import Dosificacion
from datetime import date
from sqlalchemy.exc import IntegrityError

class DosificacionService:
    
    @staticmethod
    def listar():
        return Dosificacion.query.order_by(Dosificacion.fecha_limite_emision.desc()).all()

    @staticmethod
    def listar_vigentes():
        """Lista dosificaciones vigentes (activas y dentro de fecha)"""
        return Dosificacion.query.filter(
            Dosificacion.activo == True,
            Dosificacion.fecha_limite_emision >= date.today()
        ).order_by(Dosificacion.fecha_limite_emision).all()

    @staticmethod
    def obtener(id_dosificacion):
        return db.session.get(Dosificacion, id_dosificacion)

    @staticmethod
    def obtener_dosificacion_activa():
        """Obtiene la dosificación activa principal"""
        return Dosificacion.query.filter(
            Dosificacion.activo == True,
            Dosificacion.fecha_limite_emision >= date.today()
        ).first()

    @staticmethod
    def crear(nro_autorizacion, nit_empresa, sucursal, tipo_factura, nro_inicial, nro_final, llave_dosificacion, fecha_limite_emision, cufd=None, codigo_control=None):
        if not nro_autorizacion:
            return False, "Error: El número de autorización no puede estar vacío."
        if nro_inicial > nro_final:
            return False, "Error: El número inicial no puede ser mayor al final."
        if fecha_limite_emision < date.today():
            return False, "Error: La fecha límite de emisión no puede ser pasada."
        
        try:
            # Validar autorización única
            if Dosificacion.query.filter_by(nro_autorizacion=nro_autorizacion).first():
                return False, "Error: Ya existe una dosificación con ese número de autorización."

            dosificacion = Dosificacion(
                nro_autorizacion=nro_autorizacion,
                nit_empresa=nit_empresa,
                sucursal=sucursal,
                tipo_factura=tipo_factura,
                nro_inicial=nro_inicial,
                nro_actual=nro_inicial,  # Empezar desde el inicial
                nro_final=nro_final,
                llave_dosificacion=llave_dosificacion.strip() if llave_dosificacion else None,
                fecha_limite_emision=fecha_limite_emision,
                cufd=cufd.strip() if cufd else None,
                codigo_control=codigo_control.strip() if codigo_control else None
            )
            db.session.add(dosificacion)
            
            # Desactivar otras dosificaciones del mismo tipo
            Dosificacion.query.filter(
                Dosificacion.tipo_factura == tipo_factura,
                Dosificacion.id_dosificacion != dosificacion.id_dosificacion
            ).update({Dosificacion.activo: False})
            
            db.session.commit()
            return True, "Dosificación creada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe una dosificación con ese número de autorización."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear dosificación: {str(e)}"

    @staticmethod
    def actualizar(id_dosificacion, nro_autorizacion, nro_inicial, nro_final, fecha_limite_emision, activo=True):
        try:
            dosificacion = db.session.get(Dosificacion, id_dosificacion)
            if not dosificacion:
                return False, "Dosificación no encontrada."

            dosificacion.nro_autorizacion = nro_autorizacion
            dosificacion.nro_inicial = nro_inicial
            dosificacion.nro_final = nro_final
            dosificacion.fecha_limite_emision = fecha_limite_emision
            dosificacion.activo = activo

            db.session.commit()
            return True, "Dosificación actualizada exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe una dosificación con ese número de autorización."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar dosificación: {str(e)}"

    @staticmethod
    def obtener_siguiente_numero(id_dosificacion=None):
        """Obtiene el siguiente número de factura disponible y lo incrementa"""
        try:
            if id_dosificacion:
                dosificacion = db.session.get(Dosificacion, id_dosificacion)
            else:
                dosificacion = DosificacionService.obtener_dosificacion_activa()
            
            if not dosificacion:
                return False, "No hay dosificación activa disponible."
            
            if not dosificacion.esta_vigente:
                return False, "La dosificación no está vigente."
            
            if dosificacion.nro_actual > dosificacion.nro_final:
                return False, "Se agotaron los números de factura disponibles."

            numero_actual = dosificacion.nro_actual
            dosificacion.nro_actual += 1
            db.session.commit()
            return True, numero_actual
        except Exception as e:
            db.session.rollback()
            return False, f"Error al obtener número de factura: {str(e)}"