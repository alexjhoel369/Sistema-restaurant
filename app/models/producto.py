from app import db

class Producto(db.Model):
    __tablename__ = "producto"

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categoria_producto.id_categoria", ondelete="RESTRICT"), nullable=False)
    tiempo_preparacion_minutos = db.Column(db.Integer, default=15)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    categoria = db.relationship("CategoriaProducto", back_populates="productos")
    recetas = db.relationship("Receta", back_populates="producto", lazy=True, cascade="all, delete-orphan")
    detalles_comanda = db.relationship("DetalleComanda", back_populates="producto", lazy=True)
    detalles_factura = db.relationship("FacturaDetalle", back_populates="producto", lazy=True)

    @property
    def insumos_necesarios(self):
        """Retorna lista de insumos necesarios para este producto"""
        return [receta.insumo for receta in self.recetas]

    def __repr__(self):
        return f"<Producto {self.nombre} - Bs.{self.precio}>"