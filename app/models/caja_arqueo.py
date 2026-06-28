from app import db

class CajaArqueo(db.Model):
    __tablename__ = "caja_arqueo"
    __table_args__ = (
        db.UniqueConstraint('id_sesion', 'id_metodo', name='uq_arqueo_sesion_metodo'),
    )

    id_arqueo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sesion = db.Column(db.Integer, db.ForeignKey("caja_sesion.id_sesion", ondelete="CASCADE"), nullable=False)
    id_metodo = db.Column(db.Integer, db.ForeignKey("metodo_pago.id_metodo"), nullable=False)
    monto_inicial = db.Column(db.Numeric(10, 2), default=0.00)
    monto_final = db.Column(db.Numeric(10, 2))
    monto_esperado = db.Column(db.Numeric(10, 2))
    diferencia = db.Column(db.Numeric(10, 2))

    # Relaciones
    sesion = db.relationship("CajaSesion", back_populates="arqueos")
    metodo_pago = db.relationship("MetodoPago", back_populates="arqueos")

    def __repr__(self):
        return f"<CajaArqueo Sesion {self.id_sesion} - {self.metodo_pago.nombre}>"