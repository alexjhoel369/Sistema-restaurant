from app.utils.db import db

class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    id_proveedor = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    telefono = db.Column(
        db.String(20)
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )