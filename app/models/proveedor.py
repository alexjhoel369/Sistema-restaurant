from app import db

class Proveedor(db.Model):
    __tablename__ = "proveedor"

    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    nit_ci = db.Column(db.String(20), unique=True)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    contacto_nombre = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    movimientos_inventario = db.relationship("InventarioMovimiento", back_populates="proveedor", lazy=True)

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"