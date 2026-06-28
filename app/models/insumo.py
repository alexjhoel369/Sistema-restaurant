from app import db

class Insumo(db.Model):
    __tablename__ = "insumo"

    id_insumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categoria_insumo.id_categoria"))
    unidad_medida = db.Column(db.String(20), nullable=False)
    stock_actual = db.Column(db.Numeric(10, 3), nullable=False, default=0.000)
    stock_minimo = db.Column(db.Numeric(10, 3), nullable=False, default=10.000)
    stock_maximo = db.Column(db.Numeric(10, 3), default=100.000)
    costo_unitario_promedio = db.Column(db.Numeric(10, 2), default=0.00)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    categoria = db.relationship("CategoriaInsumo", back_populates="insumos")
    recetas = db.relationship("Receta", back_populates="insumo", lazy=True)
    movimientos = db.relationship("InventarioMovimiento", back_populates="insumo", lazy=True)

    @property
    def stock_bajo(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.stock_actual <= self.stock_minimo

    @property
    def necesita_reabastecer(self):
        """Verifica si necesita reabastecimiento urgente"""
        return self.stock_actual <= (self.stock_minimo * 0.5)

    def __repr__(self):
        return f"<Insumo {self.nombre} - Stock: {self.stock_actual} {self.unidad_medida}>"