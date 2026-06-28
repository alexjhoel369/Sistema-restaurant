from app import db

class InventarioMovimiento(db.Model):
    __tablename__ = "inventario_movimiento"

    id_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey("insumo.id_insumo", ondelete="RESTRICT"), nullable=False)
    tipo_movimiento = db.Column(db.String(30), nullable=False)
    cantidad = db.Column(db.Numeric(10, 3), nullable=False)
    stock_anterior = db.Column(db.Numeric(10, 3), nullable=False)
    stock_nuevo = db.Column(db.Numeric(10, 3), nullable=False)
    costo_unitario = db.Column(db.Numeric(10, 2))
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id_proveedor", ondelete="SET NULL"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    id_comanda = db.Column(db.Integer)
    numero_factura = db.Column(db.String(50))
    motivo = db.Column(db.Text)

    # Relaciones
    insumo = db.relationship("Insumo", back_populates="movimientos")
    proveedor = db.relationship("Proveedor", back_populates="movimientos_inventario")
    usuario = db.relationship("Usuario", back_populates="movimientos_inventario")

    @property
    def es_entrada(self):
        """Verifica si es un movimiento de entrada"""
        return self.tipo_movimiento.startswith("entrada")

    @property
    def es_salida(self):
        """Verifica si es un movimiento de salida"""
        return self.tipo_movimiento.startswith("salida")

    def __repr__(self):
        return f"<Movimiento {self.tipo_movimiento} - {self.cantidad}>"