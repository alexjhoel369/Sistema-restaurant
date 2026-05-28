from app.utils.db import db

class CategoriaProducto(db.Model):
    __tablename__ = 'categoria_producto'

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)