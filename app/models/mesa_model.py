from app.utils.db import db

class Mesa(db.Model):
    __tablename__ = 'mesa'

    id_mesa = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='disponible')