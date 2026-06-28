from app import db

class FacturaDetalle(db.Model):
    __tablename__ = "factura_detalle"

    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_factura = db.Column(db.Integer, db.ForeignKey("factura.id_factura", ondelete="CASCADE"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("producto.id_producto"), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  # ✅ Ya no es GENERATED
    descuento = db.Column(db.Numeric(10, 2), default=0.00)

    # Relaciones
    factura = db.relationship("Factura", back_populates="detalles")
    producto = db.relationship("Producto", back_populates="detalles_factura")

    def __repr__(self):
        return f"<DetalleFactura {self.descripcion} - Bs.{self.subtotal}>"