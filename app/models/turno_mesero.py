from app import db

class TurnoMesero(db.Model):
    __tablename__ = "turno_mesero"

    id_turno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    fecha_fin = db.Column(db.DateTime)
    estado = db.Column(db.String(20), nullable=False, default="activo")

    # Relaciones
    usuario = db.relationship("Usuario", back_populates="turnos")
    comandas = db.relationship("Comanda", back_populates="turno", lazy=True)

    @property
    def esta_activo(self):
        """Verifica si el turno está activo"""
        return self.estado == "activo"

    def finalizar(self):
        """Finaliza el turno"""
        self.fecha_fin = db.func.current_timestamp()
        self.estado = "finalizado"

    def __repr__(self):
        return f"<TurnoMesero {self.id_turno} - {self.usuario.nombre}>"