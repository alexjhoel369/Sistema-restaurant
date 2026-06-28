from app import db
from datetime import datetime

class LogAuditoria(db.Model):
    __tablename__ = "log_auditoria"

    id_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario", ondelete="SET NULL"))
    accion = db.Column(db.String(100), nullable=False)
    tabla_afectada = db.Column(db.String(50), nullable=False)
    id_registro_afectado = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    ip_origen = db.Column(db.String(45))
    detalles = db.Column(db.JSON)
    valores_anteriores = db.Column(db.JSON)
    valores_nuevos = db.Column(db.JSON)

    # Relaciones
    usuario = db.relationship("Usuario", back_populates="logs_auditoria")

    @classmethod
    def registrar(cls, usuario_id, accion, tabla, id_registro=None, detalles=None, valores_anteriores=None, valores_nuevos=None):
        """Método helper para registrar auditoría"""
        log = cls(
            id_usuario=usuario_id,
            accion=accion,
            tabla_afectada=tabla,
            id_registro_afectado=id_registro,
            detalles=detalles,
            valores_anteriores=valores_anteriores,
            valores_nuevos=valores_nuevos
        )
        db.session.add(log)
        return log

    def __repr__(self):
        return f"<LogAuditoria {self.accion} en {self.tabla_afectada}>"