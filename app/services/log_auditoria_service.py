from app import db
from app.models.log_auditoria import LogAuditoria
from datetime import datetime, timedelta

class LogAuditoriaService:
    
    @staticmethod
    def listar(limite=1000):
        """Lista los últimos registros de auditoría"""
        return LogAuditoria.query.order_by(LogAuditoria.fecha.desc()).limit(limite).all()

    @staticmethod
    def listar_por_usuario(id_usuario, limite=500):
        return LogAuditoria.query.filter_by(id_usuario=id_usuario).order_by(LogAuditoria.fecha.desc()).limit(limite).all()

    @staticmethod
    def listar_por_tabla(tabla_afectada, limite=500):
        return LogAuditoria.query.filter_by(tabla_afectada=tabla_afectada).order_by(LogAuditoria.fecha.desc()).limit(limite).all()

    @staticmethod
    def listar_por_accion(accion, limite=500):
        return LogAuditoria.query.filter_by(accion=accion).order_by(LogAuditoria.fecha.desc()).limit(limite).all()

    @staticmethod
    def listar_por_fecha(fecha_inicio, fecha_fin, limite=1000):
        return LogAuditoria.query.filter(
            LogAuditoria.fecha >= fecha_inicio,
            LogAuditoria.fecha <= fecha_fin
        ).order_by(LogAuditoria.fecha.desc()).limit(limite).all()

    @staticmethod
    def listar_ultimas_24_horas(limite=500):
        """Lista logs de las últimas 24 horas"""
        hace_24_horas = datetime.now() - timedelta(hours=24)
        return LogAuditoria.query.filter(
            LogAuditoria.fecha >= hace_24_horas
        ).order_by(LogAuditoria.fecha.desc()).limit(limite).all()

    @staticmethod
    def obtener(id_log):
        return db.session.get(LogAuditoria, id_log)

    @staticmethod
    def registrar(usuario_id, accion, tabla_afectada, id_registro_afectado=None, 
                  detalles=None, valores_anteriores=None, valores_nuevos=None, ip_origen=None):
        """Registra una acción en la auditoría"""
        try:
            log = LogAuditoria(
                id_usuario=usuario_id,
                accion=accion,
                tabla_afectada=tabla_afectada,
                id_registro_afectado=id_registro_afectado,
                ip_origen=ip_origen,
                detalles=detalles,
                valores_anteriores=valores_anteriores,
                valores_nuevos=valores_nuevos
            )
            db.session.add(log)
            db.session.commit()
            return True, "Log registrado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al registrar log: {str(e)}"

    @staticmethod
    def limpiar_antiguos(dias=90):
        """Elimina logs más antiguos que X días"""
        try:
            fecha_limite = datetime.now() - timedelta(days=dias)
            eliminados = LogAuditoria.query.filter(
                LogAuditoria.fecha < fecha_limite
            ).delete()
            db.session.commit()
            return True, f"Se eliminaron {eliminados} registros de auditoría antiguos."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al limpiar logs: {str(e)}"