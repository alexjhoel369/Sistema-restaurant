from app import db
from app.models.turno_mesero import TurnoMesero
from app.models.usuario import Usuario
from datetime import datetime

class TurnoMeseroService:
    
    @staticmethod
    def listar():
        return TurnoMesero.query.order_by(TurnoMesero.fecha_inicio.desc()).all()

    @staticmethod
    def listar_activos():
        """Lista turnos actualmente activos"""
        return TurnoMesero.query.filter_by(estado='activo').order_by(TurnoMesero.fecha_inicio.desc()).all()

    @staticmethod
    def listar_por_mesero(id_usuario):
        return TurnoMesero.query.filter_by(id_usuario=id_usuario).order_by(TurnoMesero.fecha_inicio.desc()).all()

    @staticmethod
    def listar_por_fecha(fecha):
        """Lista turnos de una fecha específica"""
        fecha_inicio = datetime.combine(fecha, datetime.min.time())
        fecha_fin = datetime.combine(fecha, datetime.max.time())
        return TurnoMesero.query.filter(
            TurnoMesero.fecha_inicio >= fecha_inicio,
            TurnoMesero.fecha_inicio <= fecha_fin
        ).order_by(TurnoMesero.fecha_inicio).all()

    @staticmethod
    def obtener(id_turno):
        return db.session.get(TurnoMesero, id_turno)

    @staticmethod
    def obtener_turno_activo(id_usuario):
        """Obtiene el turno activo de un mesero"""
        return TurnoMesero.query.filter_by(id_usuario=id_usuario, estado='activo').first()

    @staticmethod
    def iniciar_turno(id_usuario):
        """Inicia un nuevo turno para un mesero"""
        try:
            # Verificar si ya tiene un turno activo
            turno_activo = TurnoMesero.query.filter_by(id_usuario=id_usuario, estado='activo').first()
            if turno_activo:
                return False, "Error: El mesero ya tiene un turno activo."

            # Validar que el usuario existe y es mesero
            usuario = db.session.get(Usuario, id_usuario)
            if not usuario:
                return False, "Error: El usuario no existe."
            
            # Verificar que el usuario tiene rol de mesero (id_rol=4 según los seeds)
            if usuario.id_rol != 4:
                return False, "Error: El usuario no tiene rol de mesero."

            turno = TurnoMesero(
                id_usuario=id_usuario,
                fecha_inicio=datetime.now(),
                estado='activo'
            )
            db.session.add(turno)
            db.session.commit()
            return True, "Turno iniciado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al iniciar turno: {str(e)}"

    @staticmethod
    def finalizar_turno(id_turno):
        """Finaliza un turno activo"""
        try:
            turno = db.session.get(TurnoMesero, id_turno)
            if not turno:
                return False, "Turno no encontrado."
            
            if turno.estado != 'activo':
                return False, "Error: El turno ya fue finalizado."

            turno.fecha_fin = datetime.now()
            turno.estado = 'finalizado'
            db.session.commit()
            return True, "Turno finalizado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al finalizar turno: {str(e)}"