from app.utils.db import db

class FacturaDetalle(db.Model):
    __tablename__ = 'factura_detalle'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id_factura'))
    metodo_pago = db.Column(db.String(50))
    monto = db.Column(db.Numeric(10,2))