from app import db

class MetodoPago(db.Model):
    __tablename__ = "metodo_pago"

    id_metodo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    requiere_referencia = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    arqueos = db.relationship("CajaArqueo", back_populates="metodo_pago", lazy=True)
    pagos_factura = db.relationship("FacturaPago", back_populates="metodo_pago", lazy=True)

    def __repr__(self):
        return f"<MetodoPago {self.nombre}>"