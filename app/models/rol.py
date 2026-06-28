from app import db

class Rol(db.Model):
    __tablename__ = "rol"

    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    usuarios = db.relationship("Usuario", back_populates="rol", lazy=True)

    def __repr__(self):
        return f"<Rol {self.nombre}>"