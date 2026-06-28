from app import db

class FacturaPago(db.Model):
    __tablename__ = "factura_pago"

    id_pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_factura = db.Column(db.Integer, db.ForeignKey("factura.id_factura", ondelete="CASCADE"), nullable=False)
    id_metodo = db.Column(db.Integer, db.ForeignKey("metodo_pago.id_metodo"), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    referencia = db.Column(db.String(100))
    moneda = db.Column(db.String(5), default="BOB")
    tipo_cambio = db.Column(db.Numeric(10, 4), default=1.0000)
    fecha_pago = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    factura = db.relationship("Factura", back_populates="pagos")
    metodo_pago = db.relationship("MetodoPago", back_populates="pagos_factura")

    def __repr__(self):
        return f"<Pago {self.metodo_pago.nombre} - Bs.{self.monto}>"