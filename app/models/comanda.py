from app import db

class Comanda(db.Model):
    __tablename__ = "comanda"

    id_comanda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey("mesa.id_mesa", ondelete="RESTRICT"), nullable=False)
    id_mesero = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario", ondelete="RESTRICT"), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_cliente"))
    id_turno = db.Column(db.Integer, db.ForeignKey("turno_mesero.id_turno"))
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    fecha_cierre = db.Column(db.DateTime)
    estado = db.Column(db.String(20), nullable=False, default="abierta")
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    notas = db.Column(db.Text)

    # Relaciones
    mesa = db.relationship("Mesa", back_populates="comandas")
    mesero = db.relationship("Usuario", back_populates="comandas")
    cliente = db.relationship("Cliente", back_populates="comandas")
    turno = db.relationship("TurnoMesero", back_populates="comandas")
    detalles = db.relationship("DetalleComanda", back_populates="comanda", lazy=True, cascade="all, delete-orphan")
    factura = db.relationship("Factura", back_populates="comanda", uselist=False)

    @property
    def esta_abierta(self):
        """Verifica si la comanda está abierta"""
        return self.estado == "abierta"

    def cerrar(self):
        """Cierra la comanda"""
        self.fecha_cierre = db.func.current_timestamp()
        self.estado = "cerrada"

    def __repr__(self):
        return f"<Comanda {self.id_comanda} - Mesa {self.mesa.numero}>"