from app import db

class Factura(db.Model):
    __tablename__ = "factura"
    __table_args__ = (
        db.UniqueConstraint('nro_factura', 'id_dosificacion', name='uq_nro_factura_dosificacion'),
    )

    id_factura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey("comanda.id_comanda", ondelete="RESTRICT"), nullable=False)
    id_sesion = db.Column(db.Integer, db.ForeignKey("caja_sesion.id_sesion", ondelete="RESTRICT"), nullable=False)
    id_dosificacion = db.Column(db.Integer, db.ForeignKey("dosificacion.id_dosificacion"), nullable=False)
    nro_factura = db.Column(db.BigInteger, nullable=False)
    nit_ci_cliente = db.Column(db.String(20), nullable=False)
    razon_social_cliente = db.Column(db.String(150), nullable=False)
    fecha_emision = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    descuento_porcentaje = db.Column(db.Numeric(5, 2), default=0.00)
    descuento_monto = db.Column(db.Numeric(10, 2), default=0.00)
    importe_base_credito_fiscal = db.Column(db.Numeric(10, 2), default=0.00)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    cuf = db.Column(db.String(100), unique=True, nullable=False)
    cufd = db.Column(db.String(100), nullable=False)
    codigo_control = db.Column(db.String(50))
    qr_code = db.Column(db.Text)
    leyenda = db.Column(db.Text)
    estado = db.Column(db.String(20), nullable=False, default="emitida")
    motivo_anulacion = db.Column(db.Text)
    fecha_anulacion = db.Column(db.DateTime)

    # Relaciones
    comanda = db.relationship("Comanda", back_populates="factura")
    sesion_caja = db.relationship("CajaSesion", back_populates="facturas")
    dosificacion = db.relationship("Dosificacion", back_populates="facturas")
    pagos = db.relationship("FacturaPago", back_populates="factura", lazy=True, cascade="all, delete-orphan")
    detalles = db.relationship("FacturaDetalle", back_populates="factura", lazy=True, cascade="all, delete-orphan")

    @property
    def esta_anulada(self):
        """Verifica si la factura está anulada"""
        return self.estado == "anulada"

    @property
    def monto_pagado(self):
        """Calcula el monto total pagado"""
        return sum(pago.monto for pago in self.pagos)

    @property
    def saldo_pendiente(self):
        """Calcula el saldo pendiente de pago"""
        return self.total - self.monto_pagado

    def anular(self, motivo):
        """Anula la factura"""
        self.estado = "anulada"
        self.motivo_anulacion = motivo
        self.fecha_anulacion = db.func.current_timestamp()

    def __repr__(self):
        return f"<Factura {self.nro_factura} - Bs.{self.total}>"