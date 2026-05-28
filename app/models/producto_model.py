from app.utils.db import db

class Producto(db.Model):
    __tablename__ = 'producto'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria_producto.id_categoria'))
    activo = db.Column(db.Boolean, default=True)

    categoria = db.relationship('CategoriaProducto', backref='productos')