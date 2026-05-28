from app.utils.db import db

class Inventario(db.Model):
    __tablename__ = 'inventario'

    id_inventario = db.Column(db.Integer, primary_key=True)

    id_producto = db.Column(
        db.Integer,
        db.ForeignKey('producto.id_producto')
    )

    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)

    producto = db.relationship('Producto')