from app.utils.db import db

class DetalleComanda(db.Model):
    __tablename__ = 'detalle_comanda'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey('comanda.id_comanda'))
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)

    producto = db.relationship('Producto')