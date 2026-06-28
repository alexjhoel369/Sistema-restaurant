from app import db

class CategoriaProducto(db.Model):
    __tablename__ = "categoria_producto"

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    productos = db.relationship("Producto", back_populates="categoria", lazy=True)

    def __repr__(self):
        return f"<CategoriaProducto {self.nombre}>"