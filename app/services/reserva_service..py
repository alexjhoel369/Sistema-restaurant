from app import db
from app.models.reserva import Reserva
from app.models.mesa import Mesa
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

class ReservaService:
    
    @staticmethod
    def listar():
        return Reserva.query.order_by(Reserva.fecha_hora_reserva.desc()).all()

    @staticmethod
    def listar_por_fecha(fecha):
        """Lista reservas de una fecha específica"""
        fecha_inicio = datetime.combine(fecha, datetime.min.time())
        fecha_fin = fecha_inicio + timedelta(days=1)
        return Reserva.query.filter(
            Reserva.fecha_hora_reserva >= fecha_inicio,
            Reserva.fecha_hora_reserva < fecha_fin
        ).order_by(Reserva.fecha_hora_reserva).all()

    @staticmethod
    def listar_por_cliente(id_cliente):
        return Reserva.query.filter_by(id_cliente=id_cliente).order_by(Reserva.fecha_hora_reserva.desc()).all()

    @staticmethod
    def obtener(id_reserva):
        return db.session.get(Reserva, id_reserva)

    @staticmethod
    def crear(id_mesa, id_cliente, id_usuario, fecha_hora_reserva, cantidad_personas, duracion_minutos=90, notas=None):
        try:
            # Validar mesa existente y disponible
            mesa = db.session.get(Mesa, id_mesa)
            if not mesa:
                return False, "Error: La mesa no existe."
            if not mesa.activo:
                return False, "Error: La mesa no está activa."
            
            # Validar que la fecha sea futura
            if fecha_hora_reserva < datetime.now():
                return False, "Error: La fecha de reserva debe ser futura."
            
            # Validar capacidad
            if cantidad_personas > mesa.capacidad:
                return False, f"Error: La mesa tiene capacidad para {mesa.capacidad} personas."
            
            # Validar conflicto de horario
            fecha_fin = fecha_hora_reserva + timedelta(minutes=duracion_minutos)
            conflicto = Reserva.query.filter(
                Reserva.id_mesa == id_mesa,
                Reserva.estado == 'confirmada',
                Reserva.fecha_hora_reserva < fecha_fin,
                db.func.timestampadd(db.text('MINUTE'), Reserva.duracion_minutos, Reserva.fecha_hora_reserva) > fecha_hora_reserva
            ).first()
            
            if conflicto:
                return False, "Error: La mesa ya está reservada en ese horario."

            reserva = Reserva(
                id_mesa=id_mesa,
                id_cliente=id_cliente,
                id_usuario=id_usuario,
                fecha_hora_reserva=fecha_hora_reserva,
                duracion_minutos=duracion_minutos,
                cantidad_personas=cantidad_personas,
                notas=notas.strip() if notas else None
            )
            
            # Cambiar estado de la mesa
            mesa.estado = 'reservada'
            
            db.session.add(reserva)
            db.session.commit()
            return True, "Reserva creada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear reserva: {str(e)}"

    @staticmethod
    def actualizar(id_reserva, id_mesa, fecha_hora_reserva, cantidad_personas, duracion_minutos=90, notas=None):
        try:
            reserva = db.session.get(Reserva, id_reserva)
            if not reserva:
                return False, "Reserva no encontrada."
            
            if reserva.estado != 'confirmada':
                return False, "Solo se pueden modificar reservas confirmadas."

            # Validar capacidad de nueva mesa
            mesa = db.session.get(Mesa, id_mesa)
            if not mesa:
                return False, "Error: La mesa no existe."
            if cantidad_personas > mesa.capacidad:
                return False, f"Error: La mesa tiene capacidad para {mesa.capacidad} personas."

            reserva.id_mesa = id_mesa
            reserva.fecha_hora_reserva = fecha_hora_reserva
            reserva.cantidad_personas = cantidad_personas
            reserva.duracion_minutos = duracion_minutos
            reserva.notas = notas.strip() if notas else None

            db.session.commit()
            return True, "Reserva actualizada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar reserva: {str(e)}"

    @staticmethod
    def cancelar(id_reserva, motivo=None):
        """Cancela una reserva"""
        try:
            reserva = db.session.get(Reserva, id_reserva)
            if not reserva:
                return False, "Reserva no encontrada."
            
            if reserva.estado != 'confirmada':
                return False, "Solo se pueden cancelar reservas confirmadas."

            reserva.estado = 'cancelada'
            reserva.notas = f"{reserva.notas or ''} | Cancelada: {motivo}" if motivo else reserva.notas
            
            # Liberar mesa
            mesa = db.session.get(Mesa, reserva.id_mesa)
            if mesa:
                mesa.estado = 'disponible'
            
            db.session.commit()
            return True, "Reserva cancelada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cancelar reserva: {str(e)}"

    @staticmethod
    def completar(id_reserva):
        """Marca una reserva como completada"""
        try:
            reserva = db.session.get(Reserva, id_reserva)
            if not reserva:
                return False, "Reserva no encontrada."
            
            reserva.estado = 'completada'
            db.session.commit()
            return True, "Reserva completada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al completar reserva: {str(e)}"

    @staticmethod
    def eliminar(id_reserva):
        try:
            reserva = db.session.get(Reserva, id_reserva)
            if not reserva:
                return False, "Reserva no encontrada."

            # Liberar mesa si estaba reservada
            if reserva.estado == 'confirmada':
                mesa = db.session.get(Mesa, reserva.id_mesa)
                if mesa and mesa.estado == 'reservada':
                    mesa.estado = 'disponible'

            db.session.delete(reserva)
            db.session.commit()
            return True, "Reserva eliminada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al eliminar reserva: {str(e)}"