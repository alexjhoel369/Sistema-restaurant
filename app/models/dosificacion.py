from app import db

class Dosificacion(db.Model):
    __tablename__ = "dosificacion"

    id_dosificacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nro_autorizacion = db.Column(db.BigInteger, unique=True, nullable=False)
    nit_empresa = db.Column(db.BigInteger, nullable=False)
    sucursal = db.Column(db.Integer, default=0)
    tipo_factura = db.Column(db.String(20), nullable=False, default="factura")
    nro_inicial = db.Column(db.BigInteger, nullable=False)
    nro_actual = db.Column(db.BigInteger, nullable=False)
    nro_final = db.Column(db.BigInteger, nullable=False)
    llave_dosificacion = db.Column(db.String(255))
    fecha_limite_emision = db.Column(db.Date, nullable=False)
    cufd = db.Column(db.String(100))
    codigo_control = db.Column(db.String(10))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    facturas = db.relationship("Factura", back_populates="dosificacion", lazy=True)

    @property
    def nros_disponibles(self):
        """Cantidad de números de factura disponibles"""
        return self.nro_final - self.nro_actual + 1

    @property
    def esta_vigente(self):
        """Verifica si la dosificación aún está vigente"""
        from datetime import date
        return self.activo and self.fecha_limite_emision >= date.today()

    def __repr__(self):
        return f"<Dosificacion {self.nro_autorizacion}>"