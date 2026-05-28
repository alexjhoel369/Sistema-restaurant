from app.utils.db import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'factura'

    id_factura = db.Column(db.Integer, primary_key=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey('comanda.id_comanda'))
    fecha = db.Column(db.DateTime, default=datetime.now)
    total = db.Column(db.Numeric(10,2), nullable=False)