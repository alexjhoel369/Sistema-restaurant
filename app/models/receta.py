from app import db

class Receta(db.Model):
    __tablename__ = "receta"
    __table_args__ = (
        db.UniqueConstraint('id_producto', 'id_insumo', name='uq_receta_producto_insumo'),
    )

    id_receta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey("producto.id_producto", ondelete="CASCADE"), nullable=False)
    id_insumo = db.Column(db.Integer, db.ForeignKey("insumo.id_insumo", ondelete="RESTRICT"), nullable=False)
    cantidad_requerida = db.Column(db.Numeric(10, 3), nullable=False)
    unidad_medida = db.Column(db.String(20), nullable=False)
    es_opcional = db.Column(db.Boolean, default=False)
    notas = db.Column(db.Text)

    # Relaciones
    producto = db.relationship("Producto", back_populates="recetas")
    insumo = db.relationship("Insumo", back_populates="recetas")

    def __repr__(self):
        return f"<Receta {self.producto.nombre} -> {self.insumo.nombre}>"