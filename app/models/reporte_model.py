from app.utils.db import db
from datetime import datetime

class Reporte(db.Model):
    __tablename__ = 'reporte'

    id_reporte = db.Column(
        db.Integer,
        primary_key=True
    )

    tipo = db.Column(
        db.String(50)
    )

    fecha_generacion = db.Column(
        db.DateTime,
        default=datetime.now
    )

    descripcion = db.Column(
        db.Text
    )