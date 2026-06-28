from app import db

class Mesa(db.Model):
    __tablename__ = "mesa"

    id_mesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(50))
    estado = db.Column(db.String(20), nullable=False, default="disponible")
    activo = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    comandas = db.relationship("Comanda", back_populates="mesa", lazy=True)
    reservas = db.relationship("Reserva", back_populates="mesa", lazy=True)

    @property
    def esta_disponible(self):
        """Verifica si la mesa está disponible"""
        return self.estado == "disponible"

    def __repr__(self):
        return f"<Mesa {self.numero} ({self.capacidad}p)>"