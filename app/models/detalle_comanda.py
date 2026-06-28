from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class DetalleComanda(db.Model):
    __tablename__ = "detalle_comanda"

    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey("comanda.id_comanda", ondelete="CASCADE"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("producto.id_producto", ondelete="RESTRICT"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    
    # ✅ CLAVE: server_default y FetchedValue para columnas GENERATED
    subtotal = db.Column(db.Numeric(10, 2), server_default=db.text("0.00"))
    
    estado_preparacion = db.Column(db.String(20), nullable=False, default="pendiente")
    notas = db.Column(db.Text)

    # Relaciones
    comanda = db.relationship("Comanda", back_populates="detalles")
    producto = db.relationship("Producto", back_populates="detalles_comanda")

    @property
    def esta_listo(self):
        return self.estado_preparacion == "listo"

    def __repr__(self):
        return f"<DetalleComanda {self.cantidad}x{self.producto.nombre}>"