from app.utils.db import db

class Comanda(db.Model):
    __tablename__ = 'comanda'

    id_comanda = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesa.id_mesa'))
    id_mesero = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    estado = db.Column(db.String(20), default='pendiente')
    total = db.Column(db.Numeric(10,2), default=0)

    mesa = db.relationship('Mesa')