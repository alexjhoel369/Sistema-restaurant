from app import db

class Cliente(db.Model):
    __tablename__ = "cliente"

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_documento = db.Column(db.String(5), nullable=False, default="CI")
    nit_ci = db.Column(db.String(20), unique=True, nullable=False)
    razon_social = db.Column(db.String(150), nullable=False)
    complemento = db.Column(db.String(5))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    reservas = db.relationship("Reserva", back_populates="cliente", lazy=True)
    comandas = db.relationship("Comanda", back_populates="cliente", lazy=True)

    @property
    def documento_completo(self):
        """Retorna el documento con complemento si existe"""
        if self.complemento:
            return f"{self.nit_ci}-{self.complemento}"
        return self.nit_ci

    def __repr__(self):
        return f"<Cliente {self.razon_social} ({self.nit_ci})>"