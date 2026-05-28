from app.utils.db import db
from datetime import datetime

class InventarioMovimiento(db.Model):
    __tablename__ = 'inventario_movimiento'

    id_movimiento = db.Column(db.Integer, primary_key=True)

    id_producto = db.Column(
        db.Integer,
        db.ForeignKey('producto.id_producto')
    )

    tipo = db.Column(db.String(20))
    cantidad = db.Column(db.Integer)

    fecha = db.Column(db.DateTime, default=datetime.now)

    id_proveedor = db.Column(
        db.Integer,
        db.ForeignKey('proveedor.id_proveedor')
    )

    producto = db.relationship('Producto')
    proveedor = db.relationship('Proveedor')