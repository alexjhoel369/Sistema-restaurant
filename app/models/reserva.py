from app import db

class Reserva(db.Model):
    __tablename__ = "reserva"

    id_reserva = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey("mesa.id_mesa", ondelete="RESTRICT"), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_cliente", ondelete="RESTRICT"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_hora_reserva = db.Column(db.DateTime, nullable=False)
    duracion_minutos = db.Column(db.Integer, default=90)
    cantidad_personas = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="confirmada")
    notas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    mesa = db.relationship("Mesa", back_populates="reservas")
    cliente = db.relationship("Cliente", back_populates="reservas")
    usuario = db.relationship("Usuario", back_populates="reservas")

    def __repr__(self):
        return f"<Reserva {self.id_reserva} - Mesa {self.id_mesa}>"